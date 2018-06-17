process_rankings
================

This python module calculate the volatility for each element of a ranking. It was created for the paper Ranking dynamics and volatility [1]

[1] Garcia-Zorita, C.; Rousseau, R.; Marugan-Lazaro, S.; Sanz-Casado, E. (2017). Ranking dynamics and volatility. (Paper submit to Journal of Informetrics for evaluation).

* __Author__: Marugan Lazaro, S <smarugan at pa dot uc3m dot es> 
* __Version__: 2.0


# Classes


## class `Event()`

Table with the comparisions.

**Columns:**

| element1 | position1 | element2 | position2 | period | difference | difference_memory |
|:--|:--|:--|:--|:--|:--|:--|
| type: **str** | type: **float** | type: **str** | type: **float** |type: **str**| type: **float**| type: **float** |

- element1: str

	First element to compare.

- position1: float

	Position of the first element on the period.

- element2: str

	Second element to compare.

- position2: float

	Position of the second element on the period.

- period: str

	Period of comparision.

- difference: float

	Difference between positions of element2 and element1.

- difference_memory: float

	Difference between positions of element2 and element1 before becomes tied.


### Methods:

##### def `__init__(filename)`

Constructor.

**Parameters:**

- filename: str

	Name of the HDF5 file.

## class `PartialResult()`

Table with position shifts between two elements.

**Columns:**

- element1: str

	First element.

- element2: str

	Second element.

- position_shifts: int

	Number of position shifts between this elements.

### Methods:

##### def `__init__(filename)`

Constructor.

**Parameters:**

- filename: str

	Name of the HDF5 file.


## class `Ranking()`

No documentation for this class

### Methods:

##### def `__init__(filename)`

Constructor.

## class `Table()`

Wrapper for tables of pytables.

### Methods:

##### def `__init__(tablename, filename)`

Constructor.

## class `TotalResult()`

Table with position shifts between two elements.

**Columns:**

| element | position_shifts | max_shifts | volatility |
|:--------|:----------------|:-----------|:-----------|
| type: **str**      | type: **int**	| type: **int**	| type: **float** |
| The element.  | Number of position shifts of this element. | Number of maximum position shifts for the element. | Relative volatility of the element. |


### Methods:

##### def `__init__(filename)`

Constructor.

**Parameters:**

- filename: str

	Name of the HDF5 file.

## class `Volatility()`

Class for processing the data and generate the HDF5 file with the calculation.

### Methods:

##### def `__init__(filename, delimiter=;)`

Constructor.

Initialize HDF5 tables and create the output dir for the results.

**Parameters:**

- filename: str

	Name of the csv file with the ranking

- delimiter: str

	Delimiter of the csv file. Default: ";"

##### def `process()`

Load the ranking data from the csv file and save it on Ranking table.
Generate events or comparisions and save the calculation on PartialResult and TotalResult tables.


##### def `export2csv()`

Export the tables from HDF5 format to csv.
