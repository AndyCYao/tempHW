# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv("data.csv")

plt.Figure(figsize=(15,20))
plt.plot(data)
data.hist(figsize=(15,20))


# Mann Whitney Test
# Null Hypothesis: the two groups are evenly sorted
# Alt. Hypothesis: one group is sorted higher than the other


# Chi Square Test
# Null Hyp. the categories are independent, proportion are the same

# Anova 
# Null Hyp. is that the group of data have similar mean 
# Alt  Hyp. is they have different means.
anova = stats.f_oneway(data["merge1"], data["partition_sort"], data["qs1"],
                       data["qs2"], data["qs3"], data["qs4"], data["qs5"])
print(anova)
print(anova.pvalue)

# With anova.pvalue close to 0, we reject the null the hypothesis. and there is
# difference bewteen means in the group. 

# Post Hoc Analysis. 
dataMelt = pd.melt(data)
posthoc  = pairwise_tukeyhsd(dataMelt['value'], dataMelt['variable'], alpha=0.05)
print(posthoc)

fig =  posthoc.plot_simultaneous()
# Looks like qs4 and qs5  are similar, qs2 and qs3 are similar, 
# and qs1 is the fastest. 


# Do T Test but with Bonferroni Correction  


data.boxplot()
plt.show()