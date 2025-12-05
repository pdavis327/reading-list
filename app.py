import streamlit as st
import pandas as pd
from datetime import datetime
from util.database import BookDatabase

# Initialize the database
db = BookDatabase()
db.create_table()  # Ensure the table exists

# Streamlit App Title
st.title("📚 Book Tracker App")

# Sidebar Navigation
menu = st.sidebar.radio(
    "Navigation", ["Add Book", "View Books"]
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
        year = st.number_input("Year", min_value=2024, max_value=2100, step=1, value=datetime.now().year)
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
    
    if df.empty:
        st.info("No books in the database yet. Add some books to get started!")
    else:
        # Month order for sorting
        month_order = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        
        # Sort by year (descending) then month (descending)
        df['_month_num'] = df['month'].map(month_order)
        df = df.sort_values(by=['year', '_month_num'], ascending=[False, False])
        df = df.drop(columns=['_month_num'])
        df = df.reset_index(drop=True)
        
        # Toggle between view modes
        view_mode = st.radio("View mode", ["Edit", "Sort/Browse"], horizontal=True)
        
        if view_mode == "Sort/Browse":
            st.caption("💡 Click column headers to sort. Switch to Edit mode to make changes.")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "year": st.column_config.NumberColumn("Year", format="%d"),
                    "pub_year": st.column_config.NumberColumn("Pub Year", format="%d"),
                },
            )
        else:
            st.caption("💡 Click on any cell to edit. Changes are saved when you click 'Save Changes'.")
            
            # Store original df for comparison (before any edits)
            original_df = df.copy()
            
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",  # Allows adding/deleting rows
                use_container_width=True,
                hide_index=True,
                disabled=["id"],  # Prevent editing the primary key
                column_config={
                    "id": st.column_config.NumberColumn("ID", help="Primary key (auto-generated)"),
                    "reader": st.column_config.TextColumn("Reader", max_chars=100),
                    "month": st.column_config.SelectboxColumn(
                        "Month",
                        options=["January", "February", "March", "April", "May", "June",
                                 "July", "August", "September", "October", "November", "December"],
                    ),
                    "year": st.column_config.NumberColumn("Year", min_value=2024, max_value=2100, format="%d"),
                    "title": st.column_config.TextColumn("Title", max_chars=100),
                    "author_last": st.column_config.TextColumn("Author Last", max_chars=100),
                    "author_first": st.column_config.TextColumn("Author First", max_chars=100),
                    "genre": st.column_config.TextColumn("Genre", max_chars=50),
                    "subgenre": st.column_config.TextColumn("Subgenre", max_chars=50),
                    "pub_year": st.column_config.NumberColumn("Pub Year", min_value=1850, max_value=2100, format="%d"),
                    "country": st.column_config.TextColumn("Country", max_chars=50),
                    "rating": st.column_config.NumberColumn("Rating", min_value=0.0, max_value=5.0, step=0.5),
                    "pages": st.column_config.NumberColumn("Pages", min_value=1),
                    "format": st.column_config.SelectboxColumn(
                        "Format",
                        options=["Hardcover", "Paperback", "Ebook", "Audiobook"],
                    ),
                    "keys": st.column_config.TextColumn("Keywords"),
                    "pov": st.column_config.SelectboxColumn(
                        "POV",
                        options=["First", "Third", "Omniscient"],
                    ),
                    "movie": st.column_config.CheckboxColumn("Movie"),
                },
                key="book_editor"
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("💾 Save Changes", type="primary"):
                    changes_made = False
                    
                    # Find and delete removed rows
                    original_ids = set(original_df['id'].tolist())
                    edited_ids = set(edited_df['id'].dropna().astype(int).tolist())
                    deleted_ids = original_ids - edited_ids
                    
                    for book_id in deleted_ids:
                        db.delete_book(book_id)
                        changes_made = True
                    
                    # Find rows that were modified
                    for idx, row in edited_df.iterrows():
                        if pd.isna(row['id']):
                            continue  # Skip new rows (not supported yet)
                        original_row = original_df[original_df['id'] == row['id']]
                        if not original_row.empty:
                            original_row = original_row.iloc[0]
                            # Check if any values changed
                            updates = {}
                            for col in original_df.columns:
                                if col != 'id':
                                    # Handle NaN comparisons
                                    orig_val = original_row[col]
                                    new_val = row[col]
                                    if pd.isna(orig_val) and pd.isna(new_val):
                                        continue
                                    if orig_val != new_val:
                                        updates[col] = new_val
                            
                            if updates:
                                db.update_book(row['id'], **updates)
                                changes_made = True
                    
                    if changes_made:
                        st.success("✅ Changes saved successfully!")
                        st.rerun()
                    else:
                        st.info("No changes detected.")
