# -*- coding: utf-8 -*-

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]
    #searchdata_file = "searches.json"
    searchData = pd.read_json(searchdata_file, orient='records', lines=True)
    searchData["isTreatment"] = searchData['uid'] % 2 == 0
    searchData["hasSearched"] = searchData['search_count'] > 0
    
    '''
    My contingency table shape should be
    Group Odd  AKA Treament    Has Searched  -  Has never Searched
    Group Even AKA Control     Has Searched  -  Has never searched
    '''
    
    loginDataPivot = pd.pivot_table(data=searchData, columns='hasSearched', values = 'login_count', index=['isTreatment'], aggfunc=np.count_nonzero)
    # Chi2 test Null Hypothesis is the categories are independent. ie doesn't matter what categories you're in
    # the proportion are the same. 
    # chi2, p, dof, expected = stats.chi2_contingency(loginDataPivot)
    
    '''
    Is the number of searches per user different? Use Mann Whitney U Test
    '''
    isTreatmentSearch = searchData[searchData['isTreatment'] == True]['search_count']
    notIsTreatmentSearch = searchData[searchData['isTreatment'] == False]['search_count']
    
    '''
    Instructors only
    '''
    searchDataInstructor = searchData[searchData['is_instructor'] == True]
    loginDataPivotInstructor = pd.pivot_table(data=searchDataInstructor, columns= 'hasSearched', values = 'login_count', index=['isTreatment'], aggfunc = np.count_nonzero)
    # chi2, pInstructor, dof, expected = stats.chi2_contingency(loginDataPivotInstructor)
    isTreatmentSearchInstr = searchDataInstructor[searchDataInstructor['isTreatment'] == True]['search_count']
    notIsTreatmentSearchInstr = searchDataInstructor[searchDataInstructor['isTreatment'] == False]['search_count']
    
    
    print(OUTPUT_TEMPLATE.format(
            more_users_p          = stats.chi2_contingency(loginDataPivot)[1],
            more_searches_p       = stats.mannwhitneyu(isTreatmentSearch, notIsTreatmentSearch).pvalue, 
            more_instr_p          = stats.chi2_contingency(loginDataPivotInstructor)[1], 
            more_instr_searches_p = stats.mannwhitneyu(isTreatmentSearchInstr, notIsTreatmentSearchInstr).pvalue,
            ))

if __name__ == '__main__':
    main()