import traceback

import matplotlib


from cater import Cater


if __name__ == "__main__":
    """Main Method"""

    # TODO Some better exception handling that wont result in
    #

    try:

        matplotlib.use("Agg")

        Cater().start()

    except Exception as e:

        traceback.print_exc()
