# Import data

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

#Identifying outliers

# Searches for outliers in every column from the merged_df data frame:
for col in merged_df.columns:
    column = pd.to_numeric(merged_df[col], errors='coerce')
    column.dropna(inplace=True)
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = column[(column < lower_bound) | (column > upper_bound)]
    print("Column name:", col)
    print("Number of outliers:", len(outliers))
    print("Outlier values:", outliers.values)

#Creating graphs

dates = pd.date_range(start='1960-01-01', end='1990-12-01', freq="MS")

# Plots a time series graph of the monthly growth in nominal exchange rates of Italian Lira vs USD:
plt.plot(dates, log_exchange_rates_diff)
plt.title('Monthly Growth in Nominal Exchange Rate of Italian Lira vs. United States Dollar (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Growth in nominal exchange rate (%)')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 0.09, 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.show()

# Plots a time series graph of the monthly growth in real exchange rates of Italian Lira vs USD:
plt.plot(dates, real_exchange_rate_growth[1:])
plt.title('Monthly Growth in Real Exchange Rate of Italian Lira vs. United States Dollar (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Growth in real exchange rate (%)')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 7 , 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.show()

# Plots a time series graph of the monthly indexed value of International Reserves of Italy:
plt.plot(dates, italy_reserves_index[1:])
plt.title('Monthly Indexed Value of International Reserves: Italy (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Index [Reference Value = 100]')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 3150 , 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.show()

# Plots a time series graph of the monthly indexed value of International Reserves of United States:
plt.plot(dates, us_reserves_index[1:])
plt.title('Monthly Indexed Value of International Reserves: United States (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Index [Reference Value = 100]')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 390 , 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.show()

# Plots a time series graph of the monthly indexed value of International Reserves of Italy and United States:
plt.plot(dates, italy_reserves_index[1:], label = 'Italy')
plt.plot(dates, us_reserves_index[1:], label = 'United States')
plt.title('Monthly Indexed Value of International Reserves: Italy and United States (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Index [Reference Value = 100]')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 3150 , 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.legend()
plt.show()

# Plots a time series graph of monthly inlfation:
plt.plot(dates, italy_monthly_inflation_rate[1:])
plt.title('Monthly Inflation Rate: Italy (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Inflation Rate')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 0.0321 , 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.show()

# Plots a time series graph of monthly growth in industrial production:
plt.plot(dates, industrial_production_monthly_growth)
plt.title('Monthly Growth in Industrial Production: Italy (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Monthly Growth in Industrial Production (%)')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 1.55 , 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.show()

# Plots a time series graph of the growth in industrial production vs 12 months ago:
plt.plot(dates, growth_in_industrial_production)
plt.title('Growth in Industrial Production vs. 12 Months Ago: Italy (1960-1990)')
plt.xlabel('Year')
plt.ylabel('Monthly Growth in Industrial Production (%)')
x_value = datetime.datetime.strptime('1971-08-01', '%Y-%m-%d')
plt.axvline(x=x_value, color = 'red', linestyle = '--')
plt.text(pd.to_datetime('August 1971'), 21 , 'August 1971 - Leaves Bretton Woods System', fontsize=9, zorder = 11)
plt.show()

#Creating Standard deviation table

#Converts relevant columns to numeric values:
columns_to_convert = ['Italy - 1', 'Italy - 2', 'Italy - 3', 'Italy - 7', 'United States - 1', 'United States - 2', 'United States - 3']
for col in columns_to_convert:
    merged_df.loc[2:, col] = pd.to_numeric(merged_df.loc[2:, col])

#Calculate difference between inflation in Italy versus the United States
merged_df['Difference between inflation in Italy versus the United States'] = (merged_df.iloc[2:, :]['Italy - 7'] - merged_df.iloc[2:, :]['United States - 3'])

#Adds variables:
merged_df['Italy Monthly Inflation Rate'] = italy_monthly_inflation_rate
merged_df['Monthly Growth of Nominal Exchange Rate Versus the US Dollar'] = log_exchange_rates_diff
merged_df['Monthly Growth of Real Exchange Rates Versus the US Dollar'] = real_exchange_rate_growth_series
merged_df['Monthly Growth in Industrial Production'] = industrial_production_monthly_growth

#Drop irrelevant columns
merged_df = merged_df.drop(columns = ['Italy - 1', 'Italy - 2', 'Italy - 3', 'Italy - 4','United States - 1', 'United States - 2'])

#Splitting data frame into two parts leaving ten months either side of august 1970
split1 = merged_df.iloc[:131,:]
split2 = merged_df.iloc[150:,:]

#Creating dataframe of all standard deviations before leaving Bretton Woods agreement
STDB4 = pd.DataFrame(split1.std())

#Creating dataframe of all standard deviations after leaving Bretton Woods agreement
STDafter = pd.DataFrame(split2.std())

#Merge separated dataframes on index
STDMERGE = pd.merge(STDB4, STDafter, left_index=True, right_index=True)

#Add column name for index
STDMERGE.index.name = 'Metric'

#Change column names
STDMERGE.columns=['Standard Deviation of Metric Before Leaving Bretton Woods Agreement','Standard Deviation of Metric After Leaving Bretton Woods Agreement'] 

#Create column to show ratio between standard deviation before leaving Bretton Woods Agreement and after leaving Bretton Woods Agreement
STDMERGE['Ratio or Standard Deviation After Vs Before Leaving Bretton Woods Agreement']=(STDMERGE['Standard Deviation of Metric After Leaving Bretton Woods Agreement']/STDMERGE['Standard Deviation of Metric Before Leaving Bretton Woods Agreement'])

#Rounding function to round values to 3 decimal places
def round_numeric3(x):
    if isinstance(x, (int, float)):
        return round(x, 3)
    else:
        return x

# Use previously created rounding function to round all values to no more than two decimal places
STDMERGE = STDMERGE.applymap(round_numeric3)

#Print table
STDMERGE


