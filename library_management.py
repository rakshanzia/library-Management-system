import csv

# LIST - saari books is list mein store hongi
library = []


# FUNCTION 1: LOAD BOOKS (FILE HANDLING + CSV PROCESSING)
def load_books():
    try:
        with open("library_data.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:  # LOOP
                book = {  # DICTIONARY
                    "id": int(row["id"]), 
                    "name": row["name"],
                    "author": row["author"],
                    "category": int(row["category"]),
                    "price": float(row["price"]),
                    "status": row["status"]
                }
                library.append(book)
    except FileNotFoundError:
        print("No old data found. New library started.")
    except Exception:
        print("Error reading CSV file.")


# FUNCTION 2: SAVE BOOKS (FILE HANDLING + CSV PROCESSING)
def save_books():
    with open("library_data.csv", "w", newline="") as file:
        fields = ["id", "name", "author", "category", "price", "status"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for book in library:  # LOOP
            writer.writerow(book)


# FUNCTION 3: ADD BOOK
def add_book():
    print("\n===== ADD BOOK =====")
    name = input("Enter book name: ")
    author = input("Enter author: ")
    category = input("Enter category: ")

    try:  # EXCEPTION HANDLING
        price = float(input("Enter price: "))
        if price < 0:  # CONDITION
            print("Price cannot be negative.")
            return
    except ValueError:
        print("Invalid price.")
        return

    # BOOK ID - agar library empty hai to 1, warna last ID + 1
    book_id = 1 if len(library) == 0 else library[-1]["id"] + 1

    book = {  # DICTIONARY
        "id": book_id, "name": name, "author": author,
        "category": category, "price": price, "status": "Available"
    }
    library.append(book)  # LIST
    save_books()
    print("Book has been added.")
    print("Book ID:", book_id)


# FUNCTION 4: VIEW ALL BOOKS
def view_books():
    print("\n===== ALL BOOKS =====")
    if not library:  # CONDITION
        print("No books are present in the library.")
        return

    print("-" * 90)
    print("ID | Book Name | Author | Category | Price | Status")
    print("-" * 90)
    for book in library:  # LOOP
        print(book["id"], "|", book["name"], "|", book["author"], "|",
              book["category"], "|", book["price"], "|", book["status"])
    print("-" * 90)


# FUNCTION 5: SEARCH BOOK
def search_book():
    print("\n===== SEARCH BOOK =====")
    print("1. Search by Book Name")
    print("2. Search by Author")
    print("3. Search by Category")
    choice = input("Enter your choice: ")

    if choice not in ["1", "2", "3"]:  # CONDITION
        print("Invalid choice.")
        return

    search = input("Enter search text: ").lower()
    found = False

    for book in library:  # LOOP
        if choice == "1":
            value = book["name"].lower()
        elif choice == "2":
            value = book["author"].lower()
        else:
            value = book["category"].lower()

        if search in value:  # CONDITION
            print(book["id"], "|", book["name"], "|", book["author"], "|",
                  book["category"], "|", book["price"], "|", book["status"])
            found = True

    if not found:
        print("No matching book found.")


# FUNCTION 6: ISSUE BOOK
def issue_book():
    print("\n===== ISSUE BOOK =====")
    try:  # EXCEPTION HANDLING
        book_id = int(input("Enter Book ID: "))
    except ValueError:
        print("Invalid Book ID.")
        return

    for book in library:  # LOOP
        if book["id"] == book_id:  # CONDITION
            if book["status"] == "Issued":
                print("Book is already issued.")
                return
            book["status"] = "Issued"
            save_books()
            print("Book has been issued.")
            return

    print("Book not found.")


# FUNCTION 7: RETURN BOOK
def return_book():
    print("\n===== RETURN BOOK =====")
    try:  # EXCEPTION HANDLING
        book_id = int(input("Enter Book ID: "))
    except ValueError:
        print("Invalid Book ID.")
        return

    for book in library:  # LOOP
        if book["id"] == book_id:  # CONDITION
            if book["status"] == "Available":
                print("Book is already returned.")
                return
            book["status"] = "Available"
            save_books()
            print("Book has been returned.")
            return

    print("Book not found.")


# FUNCTION 8: CATEGORY-WISE SUMMARY
def category_summary():
    print("\n===== CATEGORY-WISE SUMMARY =====")
    categories = {}  # DICTIONARY

    for book in library:  # LOOP
        category = book["category"]
        if category not in categories:
            categories[category] = 0
        if book["status"] == "Available":
            categories[category] += 1

    if not categories:  # CONDITION
        print("No books available.")
        return

    for category in categories:  # LOOP
        print(category, ":", categories[category])


# FUNCTION 9: LIBRARY STATISTICS
def library_statistics():
    print("\n===== LIBRARY STATISTICS =====")
    total_books = len(library)
    available_books = 0
    issued_books = 0
    total_value = 0
    categories = {}  # DICTIONARY

    for book in library:  # LOOP
        total_value = total_value + book["price"]

        if book["status"] == "Available":  # CONDITION
            available_books = available_books + 1
        elif book["status"] == "Issued":
            issued_books = issued_books + 1

        category = book["category"]
        if category not in categories:
            categories[category] = 0
        categories[category] = categories[category] + 1

    most_common = "None"
    if categories:  # CONDITION
        most_common = max(categories, key=categories.get)

    print("Total Books          :", total_books)
    print("Available Books      :", available_books)
    print("Issued Books         :", issued_books)
    print("Most Common Category :", most_common)
    print("Total Library Value  :", total_value)


# FUNCTION 10: AUTHOR-WISE REPORT (BONUS)
def author_report():
    print("\n===== AUTHOR-WISE REPORT =====")
    if not library:  # CONDITION
        print("No books available.")
        return

    report = {}  # DICTIONARY
    for book in library:  # LOOP
        author = book["author"]
        if author not in report:
            report[author] = {"count": 0, "value": 0}
        report[author]["count"] += 1
        report[author]["value"] += book["price"]

    print("Author               Books    Total Value")
    for author in report:  # LOOP
        print(author, "|", report[author]["count"], "|", report[author]["value"])


# FUNCTION 11: DELETE BOOK
def delete_book():
    print("\n===== DELETE BOOK =====")
    try:  # EXCEPTION HANDLING
        book_id = int(input("Enter Book ID: "))
    except ValueError:
        print("Invalid Book ID.")
        return

    for book in library:  # LOOP
        if book["id"] == book_id:  # CONDITION
            if book["status"] == "Issued":
                print("Issued book cannot be deleted.")
                return
            library.remove(book)  # LIST
            save_books()
            print("Book has been deleted.")
            return

    print("Book not found.")


# MAIN MENU
load_books()  # Pehle old books load karo

while True:  # LOOP
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Category-wise Summary")
    print("7. Library Statistics")
    print("8. Delete Book")
    print("9. Author-wise Report")
    print("10. Exit")

    try:  # EXCEPTION HANDLING
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a number from 1 to 10.")
        continue

    if choice == 1:  # CONDITIONS
        add_book()
    elif choice == 2:
        view_books()
    elif choice == 3:
        search_book()
    elif choice == 4:
        issue_book()
    elif choice == 5:
        return_book()
    elif choice == 6:
        category_summary()
    elif choice == 7:
        library_statistics()
    elif choice == 8:
        delete_book()
    elif choice == 9:
        author_report()
    elif choice == 10:
        print("Thank you for using Library Management System.")
        break
    else:
        print("Invalid choice. Try again.")
