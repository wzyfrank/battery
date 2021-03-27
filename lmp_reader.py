import pandas as pd
import os


# how many hours one day
H = 24

FILE_NAME = "data/2011-rt.csv"

# Read the LMP data, file I/O
def read_data():
    cwd = os.getcwd()
    
    # the .csv file with locational marginal prices.
    data = pd.read_csv(os.path.join(cwd, FILE_NAME), header=None, index_col=False)
    array = data.to_numpy()
    array = array / 1000
    return array

# Given the param "seed" and "day", return the prices.    
def get_lmp_with_data(data, seed, day):
    prices = data[seed][day * H: day * H + H]
    prices.reshape(1, H)
    return prices
    
# get the real-time locational marginal price
# time period： 24 hours
# interval: hour
# unit $/kWh
def get_lmp(seed, day, debug=False):
    cwd = os.getcwd()

    # the .csv file with locational marginal prices.
    data = pd.read_csv(os.path.join(cwd, FILE_NAME), header=None, index_col=False)

    array = data.to_numpy()
    prices = array[seed][day * H: day * H + H]
    
    if debug:
        print('get lmp the lmp prices are: ')
        print(prices)

    return prices

def get_dimension(debug=False):
    cwd = os.getcwd()
    
    # the .csv file with locational marginal prices.
    data = pd.read_csv(os.path.join(cwd, FILE_NAME), header=None, index_col=False)
    
    return data.shape
    
if __name__ == "__main__":
    debug = True
    # pi_energy = get_lmp(5, 200, debug)
    
    dim = get_dimension(debug)
    print(dim)
