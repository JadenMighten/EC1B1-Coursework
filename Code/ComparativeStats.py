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
split1 = merged_df.iloc[:119,:]
split2 = merged_df.iloc[138:,:]

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