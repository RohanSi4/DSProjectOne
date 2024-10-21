import os
import pandas as pd
import sqlite3

# pip install kaggle
# kaggle datasets download abdelrahmanemad594/football-players

# Function to load the CSV file into a DataFrame
def load_data(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"File not found at: {file_path}")
            return None
        
        df = pd.read_csv(file_path)
        print(f"Loaded {df.shape[0]} records with {df.shape[1]} columns from {file_path}")
        print("Columns in the dataset:", df.columns)
        return df
    except FileNotFoundError:
        print("CSV file not found. Please check the path.")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Function to modify the DataFrame (add/remove columns)
def modify_data(df):
    columns_to_remove = [] 
    df = df.drop(columns=columns_to_remove, errors='ignore')
    
    if 'Alternative positions' in df.columns:
        df['Position_Level'] = df['Alternative positions'].apply(lambda x: 'High' if 'Forward' in x else 'Low')
    else:
        print("'Alternative positions' column not found. Skipping the column modification step.")
    
    print(f"Modified data. Now has {df.shape[1]} columns.")
    return df

# Function to save DataFrame as JSON
def save_as_json(df, output_file):
    df.to_json(output_file, orient='records', lines=True)
    print(f"Data saved as JSON to {output_file}")

# Function to store data into a SQLite database
def store_in_sqlite(df, db_name='football_data.db'):
    conn = sqlite3.connect(db_name)
    df.to_sql('players', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data stored in {db_name} database successfully!")

# Function to generate a summary of the DataFrame
def generate_summary(df, stage='before'):
    if df is not None:
        print(f"Summary {stage} processing:")
        print(f"Number of records: {df.shape[0]}")
        print(f"Number of columns: {df.shape[1]}")
    else:
        print(f"No data available for summary at stage {stage}")

# Main ETL pipeline function
def etl_pipeline(csv_file, save_json=True, save_sqlite=True):
    df = load_data(csv_file)
    
    generate_summary(df, stage='before')
    
    if df is not None:
        df_modified = modify_data(df)
    
        generate_summary(df_modified, stage='after')
        
        if save_json:
            save_as_json(df_modified, 'football_data/modified_players.json')
        
        if save_sqlite:
            store_in_sqlite(df_modified, 'football_data.db')

# Run the ETL pipeline
if __name__ == '__main__':
    csv_file_path = 'football_data/sample.csv'
    etl_pipeline(csv_file_path)
