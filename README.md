
# Ranking dynamics and volatility

This repository offers a script to calculate the volatility for each element of a ranking. It was created for the paper *Ranking dynamics and volatility*. <sup>1(#footnote)</sup>

<a name="footnote"><sup>1</sup></a> Garcia-Zorita, C.; Rousseau, R.; Marugan-Lazaro, S.; Sanz-Casado, E. (2017). Ranking dynamics and volatility. Journal of Informetrics.
----------

##Example of use
We have a file data with two rankings ordered by position in two consecutive years.
This is a file delimited by tabulator with the column names "element", "year" and "position".

The script needs `python 2.7`. It can be running with:

    python  process_rankings.py --input data_file.csv

You can view the help for the arguments with `--help` option:

    usage: process_rankings.py [-h] --input INPUT [--delimiter DELIMITER]

    Calculate the volatility foreach element in a ranking.
    
    optional arguments:
      -h, --help            show this help message and exit
      --input INPUT         File with the ranking.
      --delimiter DELIMITER
                            Delimiter of the input file. Default: \t

It generate a directory with two files: the volatility calculation for each element and the number of position shifts for each pair of elements.

