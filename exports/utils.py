import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('/Users/baijiadong/Downloads/zot-music-dataset-assignment1 (1)/Records.csv')

# Swap the last two columns: 'release_date' and 'genre'
columns = list(df.columns)
columns[-2], columns[-1] = columns[-1], columns[-2]
df = df[columns]

# Save the modified DataFrame to a new CSV file
df.to_csv('/Users/baijiadong/Downloads/zot-music-dataset-assignment1 (1)/Records.csv', index=False)

print("Columns swapped and saved to Records.csv")