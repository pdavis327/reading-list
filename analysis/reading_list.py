# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: reading_list
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# %%
host = os.getenv("HOST")
port = os.getenv("PORT")
db = os.getenv("DBNAME")
user = os.getenv("USER")
table = os.getenv("READING_LIST")

# %%
# Construct the connection string
conn_string = f"dbname={db} user={user} host={host} port={port}"

# Connect to the PostgreSQL database
conn = psycopg2.connect(conn_string)


# %%
books = pd.read_csv(table)

# %%
conn.rollback()

# %%
cur = conn.cursor()

# %%
books.columns

# %%
cur.execute(
    """CREATE TABLE reading_list (
    reader VARCHAR(100),
    month VARCHAR(10),
    year INT,
    title VARCHAR(100),
    author_last VARCHAR(100),
    author_first VARCHAR(100),
    genre VARCHAR(50),
    subgenre VARCHAR(50),
    pub_year INT,
    country VARCHAR(50),
    rating NUMERIC(10, 2),
    pages INT,
    format VARCHAR(10),
    keys TEXT,
    pov VARCHAR(10),
    movie BOOLEAN
);"""
)


# %%
sql_copy = f"""COPY reading_list
FROM '{table}'
DELIMITER ','
CSV HEADER QUOTE '"';
"""


# %%
cur.execute(sql_copy)

# %%
# %%
test = """ select * from reading_list"""

# %%
cur.execute(test)

# %%
for i in cur.fetchall():
    print(i)

# %%

conn.commit()
cur.close()
