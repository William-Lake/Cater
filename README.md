# Cater

A PySimpleGUI UI for loading and exploring Pandas Dataframes.

**THIS PROJECT IS STILL IN PROGRESS. EXPECT CHANGES AND FOR THINGS TO BREAK.**


## Requirements

Python 3.8 (NOT 3.9, see note below.) installed and on your Path.

64-bit Operating System (pyarrow is used which strongly recommends it).

Preferably a virtual environment manager, but it's optional.

### Re: Python Version

At the moment (11/8/2020) Numpy doesn't play well with python 3.9. Here's a snippet from [numpy.org/news](https://numpy.org/news):

>PYTHON 3.9 IS COMING, WHEN WILL NUMPY RELEASE BINARY WHEELS?
>
>Sept 14, 2020 – Python 3.9 will be released in a few weeks. If you are an early adopter of Python versions, you may be dissapointed to find that NumPy (and other binary packages like SciPy) will not have binary wheels ready on the day of the release. It is a major effort to adapt the build infrastructure to a new Python version and it typically takes a few weeks for the packages to appear on PyPI and conda-forge.

