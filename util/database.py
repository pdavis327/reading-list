import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


class BookDatabase:
    def __init__(self):
        """Initialize database connection settings from environment variables."""
        self.dbname = os.getenv("DBNAME")
        self.user = os.getenv("USER")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.table = os.getenv("SQL_TABLE")
        self.conn = None  # Store the connection

    def connect(self):
        """Establish a database connection if not already connected."""
        if self.conn is None or self.conn.closed:
            conn_string = f"dbname={self.dbname} user={self.user} host={self.host} port={self.port}"
            self.conn = psycopg2.connect(conn_string)

    def create_table(self):
        """Create the reading_list table if it does not already exist."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id SERIAL PRIMARY KEY,
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
                )
            """
            )
            self.conn.commit()

    def insert_data(
        self,
        reader,
        month,
        year,
        title,
        author_last,
        author_first,
        genre,
        subgenre,
        pub_year,
        country,
        rating,
        pages,
        book_format,
        keys,
        pov,
        movie,
    ):
        """Insert a new book record into the database."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO {self.table} (reader, month, year, title, author_last, author_first, genre, subgenre, pub_year, country, rating, pages, format, keys, pov, movie)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    reader,
                    month,
                    year,
                    title,
                    author_last,
                    author_first,
                    genre,
                    subgenre,
                    pub_year,
                    country,
                    rating,
                    pages,
                    book_format,
                    keys,
                    pov,
                    movie,
                ),
            )
            self.conn.commit()

    def fetch_data(self):
        """Fetch all book records from the database as a Pandas DataFrame."""
        self.connect()
        df = pd.read_sql(f"SELECT * FROM {self.table}", self.conn)
        return df

    def update_book(self, book_id, **kwargs):
        """
        Update a book record by ID.
        Example usage: update_book(3, title="New Title", rating=8.5)
        """
        self.connect()
        columns = ", ".join([f"{key} = %s" for key in kwargs])
        values = list(kwargs.values()) + [book_id]

        with self.conn.cursor() as cur:
            cur.execute(f"UPDATE {self.table} SET {columns} WHERE id = %s", values)
            self.conn.commit()

    def delete_book(self, book_id):
        """Delete a book record by ID."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table} WHERE id = %s", (book_id,))
            self.conn.commit()

    def search_books(self, **kwargs):
        """
        Search for books based on given criteria.
        Example usage: search_books(title="1984", author_last="Orwell")
        """
        self.connect()
        conditions = " AND ".join([f"{key} = %s" for key in kwargs])
        values = list(kwargs.values())

        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.table} WHERE {conditions}", values)
            results = cur.fetchall()

        return results

    def close_connection(self):
        """Close the database connection."""
        if self.conn is not None:
            self.conn.close()
            self.conn = None  # Reset connection
