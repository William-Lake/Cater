import traceback
import multiprocessing

import matplotlib

from cater.cater import Cater


# Pyinstaller workaround....
def main():

    try:

        # Without this, we get repeated warnings from matplotlib
        # when generating the pandas profiling report.
        matplotlib.use("Agg")

        Cater().start()

    except Exception as e:

        traceback.print_exc()    


if __name__ == "__main__":
    """Main Method"""
    multiprocessing.freeze_support()

    main()
