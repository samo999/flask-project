import sqlite3
import pandas as pd

# Load the CSV data into a pandas dataframe
df = pd.read_csv('app/airport_codes.csv')

# Connect to SQLite database (this will create the db file if it doesn't exist)
conn = sqlite3.connect('app/airport_codes.db')

# Set the text_factory to handle Unicode characters correctly
conn.text_factory = str  # This ensures non-ASCII characters are properly handled
cursor = conn.cursor()

# Create the airports table if it doesn't exist with the correct columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS airports (
        id INTEGER PRIMARY KEY,
        ident TEXT,
        type TEXT,
        name TEXT,
        latitude_deg REAL,
        longitude_deg REAL,
        elevation_ft INTEGER,
        continent TEXT,
        iso_country TEXT,
        iso_region TEXT,
        municipality TEXT,
        scheduled_service TEXT,
        gps_code TEXT,
        iata_code TEXT,
        local_code TEXT,
        home_link TEXT,
        wikipedia_link TEXT,
        keywords TEXT
    )
''')

# Insert the data from the pandas dataframe into the SQLite database
df.to_sql('airports', conn, if_exists='replace', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("CSV data loaded into SQLite database successfully!")
