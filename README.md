
Ranking dynamics and volatility
-------------------------------

This repository offers a script to calculate the volatility for each element of a ranking. It was created for the paper *Ranking dynamics and volatility*. <sup id="a1">[1](#f1)</sup>


### Example of use

The script needs a data file with consecutive rankings ordered by position.
File should preferably be tab-delimited with the following column names: "element", "year" and "position".


The script needs `python 2.7`. It can be running with:

    python  process_rankings.py --input data_file.tsv

You can view the help for the arguments with `--help` option:

    usage: process_rankings.py [-h] --input INPUT [--delimiter DELIMITER]

    Calculate the volatility foreach element in a ranking.
    
    optional arguments:
      -h, --help            show this help message and exit
      --input INPUT         File with the ranking.
      --delimiter DELIMITER
                            Delimiter of the input file. Default: \t

Once the data processing is finished, a directory with two files will be generated: one with the volatility measure for each element and the other with number of position shifts for each pair of elements.


#### Volatility output file format

|element <sup><a id="#note-a">a</a></sup>|position shifts <sup><a id="#note-b">b</a></sup>|max. position shifts <sup><a id="#note-c">c</a></sup>|volatility <sup><a id="#note-d">d</a></sup>|num. total links <sup><a id="#note-e">e</a></sup>|num. total years <sup><a id="#note-f">f</a></sup>|
|:-|:-:|:-:|:-:|:-:|:-:|
|AFR J LIBR ARCH INFO|21|176|11.93|15|3|
|ANNU REV INFORM SCI|91|176|51.70|88|1|
|...|...|...|...|...|...|

<sup>[a](#note-a)</sup> Element in ranking.

<sup>[b](#note-b)</sup> Total number of position shifts of one element whith others.

<sup>[c](#note-c)</sup> Maximum number of possible position shifts.

<sup>[d](#note-d)</sup> Element volatility.

<sup>[e](#note-e)</sup> Number of elements having at least one position shift with the element.

<sup>[f](#note-f)</sup> Number of years in which the element appears.

#### Position shifts output file format

|event <sup><a id="#note-g">g</a></sup>|element1 <sup><a id="#note-h">h</a></sup>|element2 <sup><a id="#note-i">i</a></sup>|year1 <sup><a id="#note-j">j</a></sup>|ele1-pos-1 <sup><a id="#note-k">k</a></sup>|ele2-pos-1 <sup><a id="#note-l">l</a></sup>|year2 <sup><a id="#note-m">m</a></sup>|ele1-pos-2 <sup><a id="#note-n">n</a></sup>|ele2-pos-2 <sup><a id="#note-o">o</a></sup>|shift <sup><a id="#note-p">p</a></sup>|in_memory <sup><a id="#note-q">q</a></sup>|
|:-|:-|:-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|...|...|...|...|...|...|...|...|...|...|...|
|(2013, 2014)|AUST ACAD RES LIBR|J GLOB INF MANAG|2013|50|55|2014|60|60|0|<|
|(2014, 2015)|AUST ACAD RES LIBR|J GLOB INF MANAG|2014|60|60|2015|58|72|0||
|...|...|...|...|...|...|...|...|...|...|...|
|(2013, 2014)|J DOC|J INF SCI|2013|32|29|2014|36|26|0||
|(2014, 2015)|J DOC|J INF SCI|2014|36|26|2015|38|43|1||
|...|...|...|...|...|...|...|...|...|...|...|
|(2013, 2014)|SCIENTOMETRICS|TELEMAT INFORM|2013|8|41|2014|10|30|0||
|(2014, 2015)|SCIENTOMETRICS|TELEMAT INFORM|2014|10|30|2015|17|14|1||
|...|...|...|...|...|...|...|...|...|...|...|


<sup>[g](#note-g)</sup> **event**: Event.
<sup>[h](#note-h)</sup> **element1**: First element of comparison.
<sup>[i](#note-i)</sup> **element2**: Second element of comparison.
<sup>[j](#note-j)</sup> **year1**: First year.
<sup>[k](#note-k)</sup> **ele1-pos-1**: Position of the first element on first year.
<sup>[l](#note-l)</sup> **ele2-pos-1**: Position of the second element on first year.
<sup>[m](#note-m)</sup> **year2**: Second year.
<sup>[n](#note-n)</sup> **ele1-pos-2**: Position of the first element on second year.
<sup>[o](#note-o)</sup> **ele2-pos-2**: Position of the second element on second year.
<sup>[p](#note-p)</sup> **shift**: 1 means change of position between **year1** and **year2**.
<sup>[q](#note-q)</sup> **in_memory**: Memorized value of the position comparison between **element1** and **element2** when occurs a tie, this will value be used on the next comparison.

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
