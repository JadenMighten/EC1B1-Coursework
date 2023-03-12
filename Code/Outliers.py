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