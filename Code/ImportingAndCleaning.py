# Imports Libraries:
import pandas as pd
import numpy as np
import datetime 
import matplotlib.pyplot as plt

# Loads the two Excel sheets into data frames:
italy_df = pd.read_excel(r'/ItalyData.xlsx', sheet_name = "International Financial Statis", header=1)
us_df = pd.read_excel(r'/USData.xlsx', sheet_name = "International Financial Statis", header=1)

# Returns the number of observations in the Italy dateset:
shape = italy_df.shape
print(shape)

# Renames data frame headers:
italy_df = italy_df.rename(columns = {'Unnamed: 0':'Date','Italy':'Italy - 1', 'Italy.1':'Italy - 2', 'Italy.2':'Italy - 3', 'Italy.3':'Italy - 4'})
us_df = us_df.rename(columns = {'Unnamed: 0':'Date', 'United States':'United States - 1', 'United States.1':'United States - 2'})

# Merges the two excel files on the 'Date' column:
merged_df = pd.merge(italy_df, us_df, on='Date')

# Formats the month and year variable into a date format:
merged_df['Date'] = merged_df.iloc[1:, 0].apply(lambda x: pd.to_datetime(x, format='%b %Y').strftime('%m-%Y'))
merged_df.iloc[0, 0] = 'Month - Year'

# Converts the data from the exchange rate column into logarithms: 
exchange_rates = merged_df['Italy - 2']
exchange_rates_numeric = pd.to_numeric(exchange_rates, errors='coerce') 
exchange_rates_numeric.dropna(inplace=True) 
log_exchange_rates = np.log(exchange_rates_numeric)
log_exchange_rates.df = ({'Log Exchange Rates':log_exchange_rates})

# Calculates the differences in log exchange rates: 
log_exchange_rates = log_exchange_rates.df['Log Exchange Rates']
log_exchange_rates_diff = log_exchange_rates.diff()

# Calculates Italy's monthly inflation rate: 
italy_cpi = merged_df['Italy - 4']
italy_cpi = pd.to_numeric(italy_cpi, errors = 'coerce')
italy_monthly_inflation_rate = italy_cpi.pct_change()

# Converts the data from the industrial production column into logarithms: 
industrial_production = merged_df['Italy - 1']
industrial_production_numeric = pd.to_numeric(industrial_production, errors = 'coerce')
industrial_production_numeric.dropna(inplace = True)
log_industrial_production = np.log(industrial_production_numeric)
log_industrial_production.df = ({'Log Industrial Production':log_industrial_production})

# Calculates the monthly growth in industrial production:
industrial_production_monthly_growth = industrial_production_numeric.pct_change()

# Calculates the growth in industrial production vs 12 months ago:
merged_df.loc[1:, 'Italy - 1'] = pd.to_numeric(merged_df.loc[1:, 'Italy - 1'], errors='coerce') 
growth_in_industrial_production = (merged_df.loc[1:, 'Italy - 1'] /merged_df.loc[1:, 'Italy - 1'].shift(12)-1) * 100

# Constructs the indexes for Italy's international reserves:
italy_index_values = [100]

for i in range(1, len(merged_df)):
    italy_index_value = (merged_df.loc[i, 'Italy - 3'] / merged_df.loc[1, 'Italy - 3']) * 100
    italy_index_values.append(italy_index_value)

italy_reserves_index = italy_index_values

# Calculates the United States' monthly inflation rate: 
us_cpi = merged_df['United States - 2']
us_cpi = pd.to_numeric(us_cpi, errors = 'coerce')
us_monthly_inflation_rate = us_cpi.pct_change()

# Constructs the indexes for the United States' international reserves:
us_index_values = [100]

for i in range(1, len(merged_df)):
    us_index_value = (merged_df.loc[i, 'United States - 1'] / merged_df.loc[1, 'United States - 1']) * 100
    us_index_values.append(us_index_value)

us_reserves_index = us_index_values

# Calculates real exchange rate growth:
italy_nominal_exchange_rates = pd.to_numeric(merged_df['Italy - 2'], errors = 'coerce')
italy_cpi = pd.to_numeric(italy_cpi, errors = 'coerce')
italy_monthly_inflation_rate = italy_cpi.pct_change()
real_exchange_rate_growth = (italy_nominal_exchange_rates.pct_change() - italy_cpi.pct_change()) * 100

# Creates a series for monthly real exchange rate growth:
real_exchange_rate_growth_series = pd.Series(real_exchange_rate_growth, index=merged_df.index[1:])

# Adds the variables created above into the merged_df dataframe:
merged_df['Italy - 5'] = log_exchange_rates
merged_df['Italy - 6'] = log_exchange_rates_diff
merged_df['Italy - 7'] = italy_monthly_inflation_rate
merged_df['Italy - 8'] = log_industrial_production
merged_df['Italy - 9'] = growth_in_industrial_production
merged_df['United States - 3'] = us_monthly_inflation_rate
merged_df = merged_df[['Date','Italy - 1', 'Italy - 2', 'Italy - 3', 'Italy - 4', 'Italy - 5', 'Italy - 6', 'Italy - 7', 'Italy - 8', 'Italy - 9', 'United States - 1', 'United States - 2', 'United States - 3' ]]

# Adds labels for the variables in the merged_df data frame:
merged_df.iloc[0, 5] = 'Log Exchange Rates'
merged_df.iloc[0, 6] = 'Difference in Log Exchange Rate vs. Previous Month'
merged_df.iloc[0, 7] = 'Monthly Inflation Rate'
merged_df.iloc[0, 8] = 'Log Industrial Production'
merged_df.iloc[0, 9] = 'Growth in Industrial Production vs. 12 Months Ago'
merged_df.iloc[0, 12] = 'Monthly Inflation Rate'

# Removes NaN values from the merged_df dataframe and replaces them with '-':
merged_df = merged_df.fillna('-')

# Converts data to 2 decimal places:
def round_numeric(x):
    if isinstance(x, (int, float)):
        return round(x, 2)
    else:
        return x

merged_df = merged_df.applymap(round_numeric)

# Displays the merged_df data frame: 
display(merged_df)