import sqlite3

# ----------------- DATABASE SETUP -----------------
# Connect to the ebookstore database
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create author table
cursor.execute('''
CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT
)
''')

# Create book table (linked to author table)
cursor.execute('''
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    authorID INTEGER,
    qty INTEGER,
    FOREIGN KEY (authorID) REFERENCES author(id)
)
''')

# Insert required authors
authors = [
    (1290, 'Charles Dickens', 'England'),
    (8937, 'J.K. Rowling', 'England'),
    (2356, 'C.S. Lewis', 'Ireland'),
    (6380, 'J.R.R. Tolkien', 'South Africa'),
    (5620, 'Lewis Carroll', 'England')
]

for author in authors:
    cursor.execute('''
        INSERT OR IGNORE INTO author (id, name, country)
        VALUES (?, ?, ?)
    ''', author)

# Insert required books
books = [
    (3001, 'A Tale of Two Cities', 1290, 30),
    (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
    (3004, 'The Lord of the Rings', 6380, 37),
    (3005, "Alice’s Adventures in Wonderland", 5620, 12)
]

for book in books:
    cursor.execute('''
        INSERT OR IGNORE INTO book (id, title, authorID, qty)
        VALUES (?, ?, ?, ?)
    ''', book)

conn.commit()

# ----------------- FUNCTIONS -----------------
def enter_book():
    '''Add a new book to the database.'''
    try:
        id_str = input("Enter book ID (4 digits): ").strip()
        authorID_str = input("Enter author ID (4 digits): ").strip()

        # ---- VALIDATION FOR 4-DIGIT IDS ----
        if not (id_str.isdigit() and authorID_str.isdigit()):
            print("Error: IDs must be numeric.")
            return
        if len(id_str) != 4 or len(authorID_str) != 4:
            print("Error: Both Book ID and Author ID must be exactly 4 digits long.")
            return

        id = int(id_str)
        authorID = int(authorID_str)

        # ---- CHECK IF AUTHOR EXISTS ----
        cursor.execute("SELECT * FROM author WHERE id = ?", (authorID,))
        author = cursor.fetchone()

        if not author:
            print(f"No author found with ID {authorID}.")
            add_author = input("Would you like to add a new author? (y/n): ").lower()
            if add_author == 'y':
                name = input("Enter author’s name: ").strip()
                country = input("Enter author’s country: ").strip()
                cursor.execute('''
                    INSERT INTO author (id, name, country)
                    VALUES (?, ?, ?)
                ''', (authorID, name, country))
                conn.commit()
                print(f"Author '{name}' added successfully.")
            else:
                print("Book entry cancelled since author does not exist.")
                return

        # ---- ENTER BOOK DETAILS ----
        title = input("Enter book title: ").strip()
        qty = int(input("Enter quantity: ").strip())

        cursor.execute('''
            INSERT INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
        ''', (id, title, authorID, qty))
        conn.commit()
        print(f"Book '{title}' added successfully!")

    except ValueError:
        print("Invalid input. IDs and quantity must be numbers.")
    except Exception as e:
        print("Error adding book:", e)

def update_book():
    '''Update book or author details using INNER JOIN.'''
    cursor.execute('''
        SELECT book.id, book.title, author.id, author.name, author.country, book.qty
        FROM book
        INNER JOIN author ON book.authorID = author.id
    ''')
    books = cursor.fetchall()

    if not books:
        print("No books available to update.")
        return

    print("\nCurrent books in the database:")
    for b in books:
        print(f"ID: {b[0]}, Title: {b[1]}, Author: {b[3]}, Country: {b[4]}, Qty: {b[5]}")

    try:
        book_id = int(input("\nEnter the ID of the book you want to update: ").strip())
    except ValueError:
        print("Invalid ID. Must be a number.")
        return

    cursor.execute('''
        SELECT book.id, book.title, author.id, author.name, author.country, book.qty
        FROM book
        INNER JOIN author ON book.authorID = author.id
        WHERE book.id = ?
    ''', (book_id,))
    book = cursor.fetchone()

    if not book:
        print("No book found with that ID.")
        return

    print(f"\nBook selected: {book[1]}")
    print(f"Author: {book[3]} ({book[4]})")
    print(f"Quantity: {book[5]}")

    print("\nWhat do you want to update?")
    print("1. Quantity (default)")
    print("2. Title")
    print("3. Author’s name")
    print("4. Author’s country")

    choice = input("Choose an option (1-4, default 1): ").strip() or "1"

    if choice == "1":
        new_qty = int(input("Enter new quantity: ").strip())
        cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (new_qty, book_id))
        conn.commit()
        print(f"Quantity updated to {new_qty}.")
    elif choice == "2":
        new_title = input("Enter new title: ").strip()
        cursor.execute("UPDATE book SET title = ? WHERE id = ?", (new_title, book_id))
        conn.commit()
        print(f"Title updated to '{new_title}'.")
    elif choice == "3":
        new_name = input("Enter new author name: ").strip()
        cursor.execute("UPDATE author SET name = ? WHERE id = ?", (new_name, book[2]))
        conn.commit()
        print(f"Author’s name updated to '{new_name}'.")
    elif choice == "4":
        new_country = input("Enter new author country: ").strip()
        cursor.execute("UPDATE author SET country = ? WHERE id = ?", (new_country, book[2]))
        conn.commit()
        print(f"Author’s country updated to '{new_country}'.")
    else:
        print("Invalid option. No changes made.")


def delete_book():
    '''Delete a book from the database.'''
    try:
        book_id = int(input("Enter the ID of the book to delete: ").strip())
    except ValueError:
        print("Invalid ID. Must be a number.")
        return

    cursor.execute("SELECT * FROM book WHERE id=?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print("Book not found.")
        return

    confirm = input(f"Are you sure you want to delete '{book[1]}'? (y/n): ").lower()
    if confirm == "y":
        cursor.execute("DELETE FROM book WHERE id=?", (book_id,))
        conn.commit()
        print(f"Book '{book[1]}' deleted successfully.")
    else:
        print("Deletion cancelled.")


def search_books():
    '''Search for books by title.'''
    search_term = input("Enter part of the title to search: ").strip()
    cursor.execute("SELECT * FROM book WHERE title LIKE ?", (f"%{search_term}%",))
    results = cursor.fetchall()

    if results:
        print("\nSearch Results:")
        for book in results:
            print(f"ID: {book[0]}, Title: '{book[1]}', AuthorID: {book[2]}, Qty: {book[3]}")
    else:
        print("No books found.")


def view_all_books():
    '''Display all books with author name and country.'''
    cursor.execute('''
        SELECT book.title, author.name, author.country
        FROM book
        INNER JOIN author ON book.authorID = author.id
    ''')
    results = cursor.fetchall()

    if not results:
        print("No books found.")
        return

    print("\nDetails\n" + "-" * 50)
    for title, name, country in results:
        print(f"Title: {title}")
        print(f"Author's Name: {name}")
        print(f"Author's Country: {country}")
        print("-" * 50)

# ----------------- MAIN MENU -----------------
while True:
    print("\n--- Inventory Management Menu ---")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. View details of all books")
    print("0. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        enter_book()
    elif choice == "2":
        update_book()
    elif choice == "3":
        delete_book()
    elif choice == "4":
        search_books()
    elif choice == "5":
        view_all_books()
    elif choice == "0":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Try again.")

# Close database connection
conn.commit()
conn.close()
print("Database connection closed successfully.")
