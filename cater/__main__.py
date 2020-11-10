import traceback

import matplotlib


from cater import Cater


if __name__ == "__main__":
    """Main Method"""

    from managers.config_manager import ConfigManager

    cm = ConfigManager()

    # cm.save_info('datasets',**{'name':'test','path':'test.csv','columns':'A &&& B'})

    # cm.save_info('other',**{'a':1})

    from pathlib import Path

    # cm.save(Path('test'))

    cm.load(Path('test'))

    print(cm.get_info('datasets'))

    print(cm.get_info('other'))

    

    # try:

    #     # Without this, we get repeated warnings from matplotlib
    #     # when generating the pandas profiling report.
    #     matplotlib.use("Agg")

    #     Cater().start()

    # except Exception as e:

    #     traceback.print_exc()
