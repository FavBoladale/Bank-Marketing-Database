# Start coding...
import pandas as pd
import numpy as np

# Read in bank_marketing.csv as a pandas DataFrame.
bank_marketing = pd.read_csv("bank_marketing.csv")

# Split the data into three DataFrames
# when working with large datasets, you need to be split into smaller more manageable dataframes

# Define the columns for each table
client = bank_marketing[["client_id", "age", "job", "marital", "education", 
             "credit_default", "housing", "loan"]]
campaign = bank_marketing[["client_id", "campaign", "month", "day", 
               "duration", "pdays", "previous", "poutcome", "y"]]
economics = bank_marketing[["client_id", "emp_var_rate", "cons_price_idx", 
                "euribor3m", "nr_employed"]]

# Rename client_id in the client table
client.rename(columns={"client_id": "id"}, inplace=True)

# Rename duration, y, and campaign columns
campaign.rename(columns={"duration": "contact_duration", 
                         "y": "campaign_outcome", 
                         "campaign": "number_contacts",
                         "previous": "previous_campaign_contacts",
                         "poutcome": "previous_outcome"}, 
                         inplace=True)

# Rename euribor3m and nr_employed
economics.rename(columns={"euribor3m": "euribor_three_months", 
                          "nr_employed": "number_employed"}, 
                          inplace=True)

# Change "." to "_" and "unknown" to NumPy's null values
client["education"] = client["education"].str.replace(".", "_")
client["education"] = client["education"].replace("unknown", np.NaN)

# Remove periods from the "job" column
client["job"] = client["job"].str.replace(".", "")

# Convert "success" and "failure" to binary (1 or 0) in "previous_outcome" and "campaign_outcome"
campaign["campaign_outcome"] = campaign["campaign_outcome"].map({"yes": 1, 
                                                                 "no": 0})

# Change "nonexistent" to NumPy's null values in "previous_outcome
campaign["previous_outcome"] = campaign["previous_outcome"].replace("nonexistent", 
                                                                    np.NaN)
campaign["previous_outcome"] = campaign["previous_outcome"].map({"success": 1, 
                                                                 "failure": 0})

# Add a column called campaign_id in campaign, where all rows have a value of 1

campaign["campaign_id"] = 1

# Capitalize month and day columns
campaign["month"] = campaign["month"].str.capitalize()

# Add year column
campaign["year"] = "2022"

# Convert day to string
campaign["day"] = campaign["day"].astype(str)

# Add last_contact_date column
campaign["last_contact_date"] = campaign["year"] + "-" + campaign["month"] + "-" + campaign["day"]

# Convert to datetime
campaign["last_contact_date"] = pd.to_datetime(campaign["last_contact_date"], 
                                               format="%Y-%b-%d")

# Drop unneccessary columns
campaign.drop(columns=["month", "day", "year"], inplace=True)

# Save tables to individual csv files
client.to_csv("client.csv", index=False)
campaign.to_csv("campaign.csv", index=False)
economics.to_csv("economics.csv", index=False)

# Store and print database_design
client_table = """CREATE TABLE client
(
    id SERIAL PRIMARY KEY,
    age INTEGER,
    job TEXT,
    marital TEXT,
    education TEXT,
    credit_default BOOLEAN,
    housing BOOLEAN,
    loan BOOLEAN
);
\copy client from 'client.csv' DELIMITER ',' CSV HEADER
"""

campaign_table = """CREATE TABLE campaign
(
    campaign_id SERIAL PRIMARY KEY,
    client_id SERIAL references client (id),
    number_contacts INTEGER,
    contact_duration INTEGER,
    pdays INTEGER,
    previous_campaign_contacts INTEGER,
    previous_outcome BOOLEAN,
    campaign_outcome BOOLEAN,
    last_contact_date DATE    
);
\copy campaign from 'campaign.csv' DELIMITER ',' CSV HEADER
"""

economics_table = """CREATE TABLE economics
(
    client_id SERIAL references client (id),
    emp_var_rate FLOAT,
    cons_price_idx FLOAT,
    euribor_three_months FLOAT,
    number_employed FLOAT
);
\copy economics from 'economics.csv' DELIMITER ',' CSV HEADER
"""