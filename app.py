import streamlit as st
import pandas as pd
from util.database import BookDatabase

# Initialize the database
db = BookDatabase()
db.create_table()  # Ensure the table exists

# Streamlit App Title
st.title("📚 Book Tracker App")

# Sidebar Navigation
menu = st.sidebar.radio(
    "Navigation", ["Add Book", "View Books", "Update Book", "Delete Book"]
)

# Add Book Section
if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    with st.form("add_book_form"):
        reader = st.text_input("Reader")
        month = st.selectbox(
            "Month",
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
        )
        year = st.number_input("Year", min_value=2024, max_value=2100, step=1)
        title = st.text_input("Title")
        author_last = st.text_input("Author Last Name")
        author_first = st.text_input("Author First Name")
        genre = st.text_input("Genre")
        subgenre = st.text_input("Subgenre")
        pub_year = st.number_input(
            "Publication Year", min_value=1850, max_value=2100, step=1
        )
        country = st.text_input("Country")
        rating = st.number_input("Rating (1-5)", min_value=0.0, max_value=5.0, step=0.5)
        pages = st.number_input("Number of Pages", min_value=1, step=1)
        book_format = st.selectbox(
            "Format", ["Hardcover", "Paperback", "Ebook", "Audiobook"]
        )
        keywords = st.text_area("Keywords (comma-separated)")
        pov = st.selectbox("Point of View", ["First", "Third", "Omniscient"])
        movie = st.checkbox("Adapted to a Movie")
        submit = st.form_submit_button("Add Book")

        if submit:
            db.insert_data(
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
                keywords,
                pov,
                movie,
            )
            st.success(f"✅ '{title}' added successfully!")

# View Books Section
elif menu == "View Books":
    st.subheader("📖 View All Books")
    df = db.fetch_data()
    st.dataframe(df)

# Update Book Section
elif menu == "Update Book":
    st.subheader("✏️ Update a Book Record")
    book_id = st.number_input("Enter Book ID to Update", min_value=1, step=1)

    if st.button("Load Book Details"):
        books = db.search_books(id=book_id)
        if books:
            book = books[0]  # Load first match
            updated_title = st.text_input("Title", value=book[4])
            updated_rating = st.number_input(
                "Rating", min_value=0.0, max_value=10.0, step=0.1, value=book[11]
            )

            if st.button("Update Book"):
                db.update_book(book_id, title=updated_title, rating=updated_rating)
                st.success(f"✅ Book ID {book_id} updated successfully!")
        else:
            st.error("⚠️ No book found with that ID.")

# Delete Book Section
elif menu == "Delete Book":
    st.subheader("🗑 Delete a Book")
    book_id = st.number_input("Enter Book ID to Delete", min_value=1, step=1)

    if st.button("Delete Book"):
        db.delete_book(book_id)
        st.success(f"✅ Book ID {book_id} deleted successfully!")
