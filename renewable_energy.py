import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

## renewable energy data
Energy = pd.read_excel('data/Energy Indicators.xls', skiprows=16, skipfooter=1)
Energy = Energy[1:228].drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
colnames = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
Energy.columns = colnames

Energy['Country'] = Energy['Country'].apply(lambda x: re.sub('\d*$', '', x))
Energy['Country'] = Energy['Country'].apply(lambda x: re.sub('\s\(.*', '', x))

Energy = Energy.replace({"Republic of Korea": "South Korea",
                         "United States of America": "United States",
                         "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                         "China, Hong Kong Special Administrative Region": "Hong Kong"})
Energy = Energy.replace('...', np.NaN)

Energy[['Energy Supply', 'Energy Supply per Capita', '% Renewable']] = Energy[['Energy Supply',
                                                                               'Energy Supply per Capita',
                                                                               '% Renewable']].apply(pd.to_numeric)
Energy['Energy Supply'] = Energy['Energy Supply'] * 1e6
Energy = Energy.set_index('Country')


## GDP data
GDP = pd.read_csv('data/world_bank.csv', header=None)
GDP = GDP[4:]
GDP = GDP.rename(columns=GDP.iloc[0])
GDP = GDP[1:]
GDP = GDP.replace({"Korea, Rep.": "South Korea",
                   "Iran, Islamic Rep.": "Iran",
                   "Hong Kong SAR, China": "Hong Kong"})
GDP = GDP.set_index('Country Name')
GDP.index.names = ['Country']
GDP = GDP[[float(i) for i in range(2006, 2016)]]
GDP.columns = [str(i) for i in range(2006, 2016)]

## publication activity data
ScimEn = pd.read_excel('data/scimagojr-3.xlsx')
ScimEn = ScimEn.set_index("Country")

df = pd.merge(ScimEn, Energy, how='inner', left_index=True, right_index=True).merge(GDP, how='inner',
                                                                                    left_index=True,
                                                                                    right_index=True)

df = df.sort_values(by=['Rank'])

Top15 = df[0:15]