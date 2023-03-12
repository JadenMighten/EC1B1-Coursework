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