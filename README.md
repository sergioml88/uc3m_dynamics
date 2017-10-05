
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

<b id="f1">1</b>  Garcia-Zorita, C.; Rousseau, R.; Marugan-Lazaro, S.; Sanz-Casado, E. (2017). Ranking dynamics and volatility. *Journal of Informetrics*. [↩](#a1)
