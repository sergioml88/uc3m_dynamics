
Ranking dynamics and volatility
-------------------------------

This repository offers a python module/script to calculate the volatility for each element of a ranking. It was created for the paper *Ranking dynamics and volatility*. <sup id="a1">[1](#f1)</sup>


### Installation

The script needs `python 2.7` and some libraries:

`unicodecsv==0.14.1`

`tables==3.2.2`

`matplotlib==1.5.1`

`pandas==0.17.1`

`seaborn==0.8.1`

`numpy==1.11.0`

This libraries can be installed through pip with the requirements.txt file:

`pip install -r requirements.txt`


### Example of use

The script needs a data file with all the rankings.
File should be textplain (csv) delimited by semicolon with the following column names: "element", "period" and "position".


It can be running with:

    python  process_rankings.py --input data_file.csv

You can view the help for the arguments with `--help` option:

    usage: process_rankings.py [-h] --input INPUT [--delimiter DELIMITER]

    Calculate the volatility foreach element in a ranking.
    
    optional arguments:
      -h, --help            show this help message and exit
      --input INPUT         File with the ranking.
      --delimiter DELIMITER
                            Delimiter of the input file. Default: ";"

Once the data processing is finished, a file with format HDF5 file will be created. This contains several tables with the following data:

* The loaded ranking.
* The events (comparison for each pair of active elements).
* The number of position shifts for each pair of elements.
* The volatility measure, maximum and current position shifts for each element.

See [docs/process_rankings.md](https://github.com/smarugan/uc3m_dynamics/docs/process_rankings.md) for more information about the module <b>process_rankings</b>.

### Example of input data

#### Input ranking file

|category_jcr|period|element|position|
|:-|:-:|:-:|:-:|
|...|...|...|...|
|INFORMATION SCIENCE & LIBRARY SCIENCE|1997|J AM MED INFORM ASSN|1|
|INFORMATION SCIENCE & LIBRARY SCIENCE|1997|MIS QUART|2|
|INFORMATION SCIENCE & LIBRARY SCIENCE|1997|LIBR QUART|3|
|...|...|...|...|


Only the columns "element", "period" and "position" are required in the input file.

### Example of output data

The .h5 file generated will be on [HDF5](https://support.hdfgroup.org/HDF5/) format. You can use several tools to see the output format like [viTables](http://vitables.org/) or [h5-utilities from the HDF Group](https://support.hdfgroup.org/products/hdf5_tools/#tools).

A csv file will be generated for each output data. This files are explained below.

#### Position shifts and volatility for each element (table/file: TotalResults)


|element <sup><a id="#note-a">a</a></sup>|maximum position shifts <sup><a id="#note-b">b</a></sup>|position shifts <sup><a id="#note-c">c</a></sup>|volatility <sup><a id="#note-d">d</a></sup>|
|:-|:-:|:-:|:-:|
|...|...|...|...|
|TRANSINFORMACAO [0103-3786]|2204|256|0.1161524500907441|
|WILSON LIBR BULL [0043-5651]|2204|237|0.1075317604355717|
|Z BIBL BIBL [0044-2380]|2204|187|0.08484573502722323|
|...|...|...|...|

<sup>[a](#note-a)</sup> Element in ranking.

<sup>[b](#note-b)</sup> Maximum number of possible position shifts.

<sup>[c](#note-c)</sup> Total number of position shifts with others elements.

<sup>[d](#note-d)</sup> Element volatility.


#### Position shifts between elements (table/file: PartialResults)

|element1 <sup><a id="#note-e">e</a></sup>|element2 <sup><a id="#note-f">f</a></sup>|position shifts <sup><a id="#note-g">g</a></sup>|
|:-|:-:|:-:|
|...|...|...|
|Z BIBL BIBL [0044-2380]|TELEMAT INFORM [0736-5853]|1|
|Z BIBL BIBL [0044-2380]|TRANSINFORMACAO [0103-3786]|3|
|Z BIBL BIBL [0044-2380]|WILSON LIBR BULL [0043-5651]|1|
|...|...|...|


<sup>[e](#note-e)</sup> **element1**: First element of comparison.

<sup>[g](#note-g)</sup> **element2**: Second element of comparison.

<sup>[f](#note-f)</sup> **position_shifts**: Position of the first element on first period.


#### Difference between elements' positions foreach period (table/file: Event)

|element1 <sup><a id="#note-g">g</a></sup>|position1 <sup><a id="#note-h">h</a></sup>|element2 <sup><a id="#note-i">i</a></sup>|position2 <sup><a id="#note-j">j</a></sup>|period <sup><a id="#note-k">k</a></sup>|difference <sup><a id="#note-l">l</a></sup>|difference_memory <sup><a id="#note-m">m</a></sup>
|:-|:-:|:-:|:-:|:-:|:-:|:-:|
|...|...|...|...|...|...|...|
|Z BIBL BIBL [0044-2380]|1222|TRANSINFORMACAO [0103-3786]|1228|2015|6|0|
|Z BIBL BIBL [0044-2380]|1312|TRANSINFORMACAO [0103-3786]|1304|2016|-8|0|
|Z BIBL BIBL [0044-2380]|43|WILSON LIBR BULL [0043-5651]|47|1997|4|0|
|...|...|...|...|...|...|...|


<sup>[e](#note-g)</sup> **element1**: First element of comparison.

<sup>[f](#note-f)</sup> **position1**: Position of the first element on first period.

<sup>[g](#note-g)</sup> **element2**: Second element of comparison.

<sup>[h](#note-h)</sup> **position2**: Position of the second element on first period.

<sup>[i](#note-i)</sup> **period**: Period of comparision.

<sup>[j](#note-j)</sup> **difference**: Difference between position of element2 and element1.

<sup>[k](#note-k)</sup> **difference_memory**: Difference between position of element2 and element1 before becomes tied.



### License

    Copyright (C) 2017 Sergio Marugán Lázaro, LEMI-UC3M

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

<b id="f1">1</b>  Garcia-Zorita, C.; Rousseau, R.; Marugan-Lazaro, S.; Sanz-Casado, E. (2017). Ranking dynamics and volatility. (Paper submit to *Journal of Informetrics* for evaluation). [↩](#a1)
