# -*- coding: utf-8 -*-
from implementations import all_implementations
import time
import numpy as np
import pandas as pd

def main():
    tests = 100
    resultTotal = [];
    sorts = all_implementations
    for test in range(tests):
        random_array = np.random.randint(10000, size=10000)
        result = {};
        for sort in sorts:
            start = time.time()
            res = sort(random_array)
            end = time.time()
            result[sort.__name__]=end - start
        resultTotal.append(result)
    data = pd.DataFrame(resultTotal)
    data.to_csv('data.csv', index=False)

if __name__ == '__main__':
    main()


