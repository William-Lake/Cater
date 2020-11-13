import traceback

import matplotlib


from cater import Cater


if __name__ == "__main__":
    """Main Method"""

    try:

        # Without this, we get repeated warnings from matplotlib
        # when generating the pandas profiling report.
        matplotlib.use("Agg")

        Cater().start()

    except Exception as e:

        traceback.print_exc()
