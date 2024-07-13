import pandas as pd
import matplotlib.pyplot as plt

# List of CSV file paths
csv_files = ['/content/API_SP.POP.TOTL_DS2_en_csv_v2_23.csv',
             '/content/Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_23.csv',
             '/content/Metadata_Indicator_API_SP.POP.TOTL_DS2_en_csv_v2_23.csv']

# Initialize an empty list to store dataframes
dataframes = []

# Loop through each file and read the contents
for file in csv_files:
    try:
        df = pd.read_csv(file, skiprows=4, encoding='latin1')
        if not df.empty:
            dataframes.append(df)
        else:
            print(f"File {file} is empty.")
    except pd.errors.EmptyDataError:
        print(f"File {file} has no data or columns to parse.")

# Assuming the first file is the main data file
if dataframes:
    main_df = dataframes[0]
    # Inspect the main DataFrame
    print(main_df.head())

    # List of aggregated categories to exclude
    exclude_list = [
        'World', 'IDA & IBRD total', 'Low & middle income', 'Middle income',
        'IBRD only', 'Early-demographic dividend', 'Lower middle income',
        'Upper middle income', 'East Asia & Pacific', 'Late-demographic dividend',
        'High income', 'Low income', 'Post-demographic dividend', 'Sub-Saharan Africa',
        'OECD members', 'Sub-Saharan Africa (IDA & IBRD countries)', 'Europe & Central Asia',
        'Latin America & the Caribbean', 'South Asia', 'Middle East & North Africa',
        'North America'
    ]

    # Select relevant columns (Country Name and the most recent year)
    latest_year = main_df.columns[-2]  # Second last column is the latest year with data
    population_data = main_df[['Country Name', latest_year]].dropna()

    # Rename columns for clarity
    population_data.columns = ['Country', 'Population']

    # Exclude aggregated categories
    population_data = population_data[~population_data['Country'].isin(exclude_list)]

    # Convert Population column to numeric
    population_data['Population'] = pd.to_numeric(population_data['Population'], errors='coerce')

    # Drop rows with invalid population data
    population_data = population_data.dropna()

    # Sort data by population in descending order
    population_data = population_data.sort_values(by='Population', ascending=False)

    # Plot the data
    plt.figure(figsize=(14, 7))
    plt.bar(population_data['Country'][:10], population_data['Population'][:10])  # Top 10 countries by population
    plt.xlabel('Country')
    plt.ylabel('Population')
    plt.title('Top 10 Countries by Population')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("No valid dataframes to process.")
