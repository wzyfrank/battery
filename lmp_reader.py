import pandas as pd
import os


# how many hours one day
H = 24


# get the real-time locational marginal price
# time period： 24 hours
# interval: hour
# unit $/kWh
def get_lmp(sample, day, debug=False):
    cwd = os.getcwd()

    # the .csv file with locational marginal prices.
    data = pd.read_csv(os.path.join(cwd, "data/files/2011-rt.csv"), header=None, index_col=False)

    array = data.to_numpy()
    prices = array[sample][day * H: day * H + H]
    prices = prices / 1000

    if debug:
        print('get lmp the lmp prices are: ')
        print(prices)

    return prices