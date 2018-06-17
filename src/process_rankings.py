#!/usr/bin/python

"""
This python module calculate the volatility for each element of a ranking. It was created for the paper Ranking dynamics and volatility [1]

[1] Garcia-Zorita, C.; Rousseau, R.; Marugan-Lazaro, S.; Sanz-Casado, E. (2017). Ranking dynamics and volatility. (Paper submit to Journal of Informetrics for evaluation).
"""

__author__ = "Sergio Marugan Lazaro <smarugan at pa dot uc3m dot es>"
__version__ = 2.0

import argparse
import unicodecsv as csv
import sys
import os
from os.path import basename
import re
from sys import exit
import tables


# Progress bar
# https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progressbar(count, total, suffix=''):
        bar_len = 50
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '#' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] [%s/%s] %s%s %s\r' % (bar, count, total, percents, '%', suffix))
        sys.stdout.flush()    # As suggested by Rom Ruben


class Table(tables.Table):
    """
    Wrapper for tables of pytables.
    """
    filters = tables.Filters(complib="lzo", complevel=1, shuffle=True)
    #valid_types = [attr[0] for attr in inspect.getmembers(tables.description) if attr[0].endswith("Col")]

    """
    __init__(self, tablename, filename)

    Parameters
    ----------
    tablename: str
        Name of the table
    filename: str
        Name of the HDF5 file.
    """
    def __init__(self, tablename, filename):
        self.tablename = tablename
        self.file = tables.open_file(filename, mode="a", title=tablename)

        try:
            self.group = self.file.get_node("/default")
        except tables.exceptions.NoSuchNodeError:
            self.group = self.file.create_group("/", "default")

        try:
            self.file.remove_node("/default", tablename)
        except tables.exceptions.NoSuchNodeError:
            pass

        self.description = dict(self.__get_description())

        tables.Table.__init__(self, parentnode=self.group, 
                                                    name=self.tablename, 
                                                    description=self.description,
                                                    title=tablename, 
                                                    expectedrows=9999999,
                                                    filters=self.filters)

        #self.file.create_table(self.group, tablename, self.description)

    # Method from simpletable:
    # url: https://bitbucket.org/brentp/biostuff/src/default/simpletable/simpletable.py
    def __get_description(self):
        # pull the description from the attrs
        for attr_name in dir(self):
            if attr_name[0] == '_': continue
                
            try:
                attr = getattr(self, attr_name)
            except:
                continue

            if isinstance(attr, tables.Atom):
                yield attr_name, attr

    #def __get_description(self):
    #    return { attr[0]:attr[1] for attr in inspect.getmembers(self) if type(attr[1]).__name__ in self.valid_types }

"""
Table with the ranking data.

Columns
-------
element: str
    Element of the ranking.
period: str
    Period of the ranking.
position: float
    Position of this element on this period.
"""
class Ranking(Table):

    element = tables.StringCol(itemsize=100)
    period = tables.StringCol(itemsize=20)
    position = tables.Float64Col()

    """
    Parameters
    ----------
    filename: str
        Name of the HDF5 file.
    """
    def __init__(self, filename):

        Table.__init__(self, "Ranking", filename)

        self.cols.period.create_index(kind="full")
        self.cols.element.create_index(kind="full")

    """
    Load the content of the csv file to a table in the HDF5 file.

    Parameters
    ----------
    filename: str
        Name of the csv file with the ranking
    delimiter: str
        Delimiter of the csv file. Default: ";"
    """
    def load_csv(self, filename, delimiter=";"):
        with open(filename, 'r') as df:
            headers = df.readline().replace('"', '').replace('\r', '').replace('\n', '').split(delimiter)

            if len(headers) < 3:
                raise Exception("ERROR: El ficher no tiene un separador valido \"%s\" o no se ha especificado el caracter separador." % delimiter)

            valid_colums = ["element", "period", "position"]
            for valid_colum in valid_colums:
                if not valid_colum in headers:
                    print "Columns: ", headers
                    raise Exception("ERROR: El fichero \"%s\" no contiene la columna requerida: \"%s\"." % (filename, valid_colum))

            reader = csv.DictReader(df, delimiter=delimiter, fieldnames=headers)
            for row in reader:
                #print row
                self.row["element"] = row["element"]
                self.row["period"] = str(row["period"])
                self.row["position"] = float(row["position"])
                self.row.append()
            self.flush()

        #Table.copy(self, newname="Ranking_sorted", sortby="element", propindexes=True)


class Event(Table):
    """
    Table with the comparisions.

    Columns
    -------
    element1: str
        First element to compare.
    position1: float
        Position of the first element on the period.
    element2: str
        Second element to compare.
    position2: float
        Position of the second element on the period.
    period: str
        Period of comparision.
    difference: float
        Difference between positions of element2 and element1.
    difference_memory: float
        Difference between positions of element2 and element1 before becomes tied.
    """
    element1 = tables.StringCol(itemsize=100)
    position1 = tables.Float64Col()

    element2 = tables.StringCol(itemsize=100)
    position2 = tables.Float64Col()

    period = tables.StringCol(itemsize=20)

    # Difference between positions of element2 and element1
    difference = tables.Float64Col()
    # Keep the difference before becomes tied
    difference_memory = tables.Float64Col(dflt=0)

    def __init__(self, filename):
        """
        Parameters
        ----------
        filename: str
            Name of the HDF5 file.
        """
        Table.__init__(self, "Event", filename)

        self.cols.period.create_index(kind="full")
        self.cols.element1.create_index(kind="full")
        self.cols.element2.create_index(kind="full")


class PartialResult(Table):
    """
    Table with position shifts between two elements.

    Columns
    -------
    element1: str
        First element.
    element2: str
        Second element.
    position_shifts: int
        Number of position shifts between this elements.
    """
    element1 = tables.StringCol(itemsize=100)
    element2 = tables.StringCol(itemsize=100)
    position_shifts = tables.Int32Col()

    def __init__(self, filename):
        """
        Parameters
        ----------
        filename: str
            Name of the HDF5 file.
        """
        Table.__init__(self, "PartialResult", filename)

        self.cols.element1.create_index(kind="full")
        self.cols.element2.create_index(kind="full")

class TotalResult(Table):
    """
    Table with position shifts between two elements.

    Columns
    -------
    element: str
        The element.
    position_shifts: int
        Number of position shifts between of this element.
    max_shifts: int
        Number of maximum position shifts for the element.
    volatility: float
        Relative volatility of the element.
    """
    element = tables.StringCol(itemsize=100)
    position_shifts = tables.Int32Col()
    max_shifts = tables.Int32Col()
    volatility = tables.Float64Col()

    def __init__(self, filename):
        """
        Parameters
        ----------
        filename: str
            Name of the HDF5 file.
        """
        Table.__init__(self, "TotalResult", filename)

        self.cols.element.create_index(kind="full")


class Volatility:
    """
    Class for processing the data and generate the HDF5 file with the calculation.

    """
    # List of periods
    periods = []
    # List of elements with the active years
    elements = {}

    # Outpur dir
    output_dir = 'output'

    def __init__(self, filename, delimiter=";"):
        """
        Initialize HDF5 tables and create the output dir for the results.

        Parameters
        ----------
        filename: str
            Name of the csv file with the ranking
        delimiter: str
            Delimiter of the csv file. Default: ";"
        """
        self.filename = filename
        self.delimiter = delimiter

        dirname, name = os.path.split(self.filename)
        basename = '.'.join(name.split(".")[:-1])
        slugname = ''.join([c if re.match(r"[a-zA-Z_0-9]", c) else "_" for c in basename])

        try:
            os.mkdir(os.path.join(self.output_dir))
        except OSError as e:
            if (e.errno != 17):
                print "ERROR: Output dir cannot be created."
                exit(1)

        slugname = os.path.join(self.output_dir, '%s.h5' % slugname)
        self.ranking = Ranking(slugname)
        self.event = Event(slugname)
        self.partial_result = PartialResult(slugname)
        self.total_result = TotalResult(slugname)

    def __generate_events(self):
        """
        Generate events or comparisions foreach pair of elements. Treat tied elements.

        Save it into Event table.
        """
        total_periods = len(self.periods)
        indx_periods = [i for i in range(0, total_periods, 1)]
        progress = 0
        total_progress = len(self.elements)
        print
        print "TOTAL PERIODS = ", total_periods
        print "TOTAL ELEMENTS = ", len(self.elements)
        print
        print "Comparing elements..."

        for ele1 in sorted(self.elements):
            for ele2 in sorted(self.elements):
                if (ele1 == ele2):
                    continue

                for period in self.periods:
                    if not period in self.elements[ele1] or \
                        not period in self.elements[ele2]:
                            continue

                    element1 = self.ranking.read_where("(element == '%s') & (period == '%s')" % (ele1, period))[0]
                    element2 = self.ranking.read_where("(element == '%s') & (period == '%s')" % (ele2, period))[0]

                    self.event.row["period"] = element1["period"]
                    self.event.row["element1"] = element1["element"]
                    self.event.row["position1"] = element1["position"]
                    self.event.row["element2"] = element2["element"]
                    self.event.row["position2"] = element2["position"]

                    diff = element2["position"]-element1["position"]
                    self.event.row["difference"] = diff

                    self.event.row.append()

            progressbar(progress, total_progress)
            progress += 1

        progressbar(progress, total_progress)

        self.event.flush()

        # When tied take the difference of the previous event
        for tied in self.event.where("difference == 0"):
            indx_period = self.periods.index(tied["period"])
            # Avoid first elements and search before become tied
            while (indx_period > 0):
                indx_period -= 1
                previous_period = self.periods[indx_period]
                # Both are active elements
                if (not previous_period in self.elements[tied["element1"]] or \
                    not previous_period in self.elements[tied["element2"]]):
                    break

                previous = self.event.read_where("(element1 == '%(element1)s') & (element2 == '%(element2)s') & \
                    (period == '%(period)s')" %
                    {
                        'period': previous_period,
                        'element1': tied["element1"],
                        'element2': tied["element2"],
                    })

                if(previous["difference"] != 0):
                    tied["difference_memory"] = previous["difference"]
                    tied.update()
                    break
                else:
                    continue

        self.event.flush()

    def __get_position_shift(self, element1, element2, period1, period2):
        """
        Check if there is a position shift between element1 and element2 on period1 and period2.

        Parameters
        ----------
        element1: str
            First element to compare.
        element2: str
            Second element to compare.
        period1: str
            First period to compare.
        period2: str
            Second period to compare.

        Returns
        -------
        int
            Position shift. 1 means there is one position shift
        """
        # element1 was active and become inactive or
        # element1 was inactive and become active
        if ((period1 in self.elements[element1] and period2 not in self.elements[element1]) or \
            (period1 not in self.elements[element1] and period2 in self.elements[element1])):
            return 1

        # element2 was active and become inactive or
        # element2 was inactive and become active
        if ((period1 in self.elements[element2] and period2 not in self.elements[element2]) or \
            (period1 not in self.elements[element2] and period2 in self.elements[element2])):
            return 1

        match1 = self.event.read_where("(element1 == '%s') & (element2 == '%s') & (period == '%s')" % (element1, element2, period1))
        match2 = self.event.read_where("(element1 == '%s') & (element2 == '%s') & (period == '%s')" % (element1, element2, period2))

        if (match1["difference"] > 0 and match2["difference"] < 0) or \
            (match1["difference"] < 0 and match2["difference"] > 0):
            return 1

        # Check ties on period1 -> Use memory
        if (match1["difference"] == 0 and match1["difference_memory"] > 0 and match2["difference"] < 0) or \
            (match1["difference"] == 0 and match1["difference_memory"] < 0 and match2["difference"] > 0):
            return 1

        # Check ties on period2 -> Use memory
        if (match2["difference"] == 0 and match2["difference_memory"] > 0 and match1["difference"] < 0) or \
            (match2["difference"] == 0 and match2["difference_memory"] < 0 and match1["difference"] > 0):
            return 1

        # Otherwise return 0
        return 0

    def process(self):
        """
        Load the ranking data from the csv file and save it on Ranking table.
        Generate events or comparisions and save the calculation on PartialResult and TotalResult tables.
        """
        self.ranking.load_csv(self.filename, self.delimiter)

        for row in self.ranking.iterrows():
            if row['period'] not in self.periods:
                self.periods.append(row['period'])

            if row['element'] not in self.elements:
                self.elements[row['element']] = []

            if not row['period'] in self.elements[row['element']]:
                self.elements[row['element']].append(row['period'])

        self.periods.sort()

        print
        print "PERIODS = ", self.periods

        # Generate the events
        self.__generate_events()

        print
        print
        print "Calculating position shifts..."
        progress = 0
        total_progress = len(self.elements)
        # Calc the partial volatility
        for ele1 in sorted(self.elements):
            self.total_result.row["element"] = ele1
            self.total_result.row["position_shifts"] = 0
            for ele2 in sorted(self.elements):
                if (ele1 == ele2):
                    continue

                total_shifts = 0
                for indx in xrange(0, len(self.periods)-1, 1):
                    event_shift = self.__get_position_shift(ele1, ele2, self.periods[indx], self.periods[indx+1])
                    total_shifts += event_shift

                self.partial_result.row["element1"] = ele1
                self.partial_result.row["element2"] = ele2
                self.partial_result.row["position_shifts"] = total_shifts
                self.partial_result.row.append()

                self.total_result.row["position_shifts"] += total_shifts

            self.total_result.row["max_shifts"] = ((len(self.elements)-1) * (len(self.periods)-1))
            self.total_result.row["volatility"] = self.total_result.row["position_shifts"]*1.0 / ((len(self.elements)-1) * (len(self.periods)-1))
            self.total_result.row.append()
            progressbar(progress, total_progress)
            progress += 1

        self.partial_result.flush()
        self.total_result.flush()
        progressbar(progress, total_progress)
        print
        print

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Calculate the volatility foreach element in a ranking.')
    parser.add_argument('--input', dest='input', type=str, required=True, help='File with the ranking.')
    parser.add_argument('--delimiter', dest='delimiter', type=str, default=';', help='Delimiter of the input file. Default: ";"')

    args = parser.parse_args()

    inputfile = args.input
    delimiter = args.delimiter

    if (not os.path.isfile(inputfile)):
        print
        print 'ERROR: File \'%s\' not found.' % inputfile
        exit(1)

    volatility = Volatility(filename=inputfile, delimiter=delimiter)
    volatility.process()
    #volatility.draw()


