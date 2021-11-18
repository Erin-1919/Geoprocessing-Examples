import pandas as pd

df1 = pd.DataFrame({'A': [None, 0, 1, 4], 'B': [2, None, 3, 5], 'c' : [1,2,3,4]})
df1 = df1.set_index('c')

df2 = pd.DataFrame({'A': [3,2,1], 'B': [3,4,5], 'c' : [3,2,1]})
df2 = df2.set_index('c')

df1
df2
df3 = df2.combine_first(df1)
df3
