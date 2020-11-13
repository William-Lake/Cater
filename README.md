# Cater

A PySimpleGUI UI for loading and exploring Pandas Dataframes.

**THIS PROJECT IS STILL IN PROGRESS. EXPECT CHANGES AND FOR THINGS TO BREAK.**


## Requirements

Python 3.8 (NOT 3.9, see note below.) installed and on your Path.

64-bit Operating System (pyarrow is used which strongly recommends it).

Preferably a virtual environment manager, but it's optional.

## Usage

`python cater`

In the future this section will contain screenshots/gifs and some better examples of what Cater can do.

## Libraries

This project was not created from scratch, it stands on the shoulders of a lot of other people. Here's the list of libraries I'm using in Cater (in no particular order) and where you can find them. Thank you to everyone who created them, and made them available for us all to use.

- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/)
- [pandas](https://pandas.pydata.org/)
- [datacompy](https://github.com/capitalone/datacompy)
- [black](https://github.com/psf/black)
- [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)
- [pandasql](https://github.com/yhat/pandasql/)
- [sqlparse](https://github.com/andialbrecht/sqlparse)
- [pyarrow](https://arrow.apache.org/)
- [tabulate](https://github.com/astanin/python-tabulate)
- [dataset](https://github.com/pudo/dataset)

### Re: Python Version

At the moment (11/8/2020) Numpy doesn't play well with python 3.9. Here's a snippet from [numpy.org/news](https://numpy.org/news):

>PYTHON 3.9 IS COMING, WHEN WILL NUMPY RELEASE BINARY WHEELS?
>
>Sept 14, 2020 – Python 3.9 will be released in a few weeks. If you are an early adopter of Python versions, you may be dissapointed to find that NumPy (and other binary packages like SciPy) will not have binary wheels ready on the day of the release. It is a major effort to adapt the build infrastructure to a new Python version and it typically takes a few weeks for the packages to appear on PyPI and conda-forge.



## Accessibility

As this project evolves I will be doing my best to meet accesibility standards, but if there's something I've missed/something that would make Cater easier for you to use please reach out and I will work with you to make it happen.