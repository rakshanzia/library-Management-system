from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

CSV_FILE = "library_data.csv"


# -------------------------
# CSV FILE SETUP
# -------------------------

def create_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "id",
                "title",
                "author",
                "category",
                "status",
                "student"
            ])


def read_books():
    create_file()

    books = []

    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            books.append(row)

    return books


def save_books(books):
    with open(CSV_FILE, "w", newline="") as file:

        fieldnames = [
            "id",
            "title",
            "author",
            "category",
            "status",
            "student"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(books)


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():

    books = read_books()

    total_books = len(books)

    available_books = 0
    issued_books = 0

    for book in books:

        if book["status"] == "Available":
            available_books += 1

        if book["status"] == "Issued":
            issued_books += 1

    categories = {}

    for book in books:

        category = book["category"]

        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    return render_template(
        "index.html",
        books=books,
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books,
        categories=categories,
        message=""
    )


# -------------------------
# ADD BOOK
# -------------------------

@app.route("/add_book", methods=["POST"])
def add_book():

    books = read_books()

    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]

    if title == "" or author == "" or category == "":
        return redirect(url_for("home"))

    new_id = 1

    if len(books) > 0:

        ids = []

        for book in books:
            ids.append(int(book["id"]))

        new_id = max(ids) + 1

    new_book = {
        "id": str(new_id),
        "title": title,
        "author": author,
        "category": category,
        "status": "Available",
        "student": ""
    }

    books.append(new_book)

    save_books(books)

    return redirect(url_for("home"))


# -------------------------
# SEARCH BOOK
# -------------------------

@app.route("/search")
def search():

    books = read_books()

    keyword = request.args.get("keyword", "").lower()

    results = []

    for book in books:

        if (
            keyword in book["title"].lower()
            or keyword in book["author"].lower()
            or keyword in book["category"].lower()
        ):
            results.append(book)

    total_books = len(books)

    available_books = 0
    issued_books = 0

    for book in books:

        if book["status"] == "Available":
            available_books += 1

        if book["status"] == "Issued":
            issued_books += 1

    categories = {}

    for book in books:

        category = book["category"]

        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    return render_template(
        "index.html",
        books=results,
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books,
        categories=categories,
        message="Search Results"
    )


# -------------------------
# ISSUE BOOK
# -------------------------

@app.route("/issue_book", methods=["POST"])
def issue_book():

    books = read_books()

    book_id = request.form["book_id"]
    student = request.form["student"]

    for book in books:

        if book["id"] == book_id:

            if book["status"] == "Available":

                book["status"] = "Issued"
                book["student"] = student

            break

    save_books(books)

    return redirect(url_for("home"))


# -------------------------
# RETURN BOOK
# -------------------------

@app.route("/return_book", methods=["POST"])
def return_book():

    books = read_books()

    book_id = request.form["book_id"]

    for book in books:

        if book["id"] == book_id:

            if book["status"] == "Issued":

                book["status"] = "Available"
                book["student"] = ""

            break

    save_books(books)

    return redirect(url_for("home"))


# -------------------------
# DELETE BOOK
# -------------------------

@app.route("/delete/<book_id>")
def delete_book(book_id):

    books = read_books()

    new_books = []

    for book in books:

        if book["id"] != book_id:
            new_books.append(book)

    save_books(new_books)

    return redirect(url_for("home"))


# -------------------------
# CATEGORY SUMMARY
# -------------------------

@app.route("/summary")
def summary():

    books = read_books()

    categories = {}

    for book in books:

        category = book["category"]

        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    total_books = len(books)

    available_books = 0
    issued_books = 0

    for book in books:

        if book["status"] == "Available":
            available_books += 1

        if book["status"] == "Issued":
            issued_books += 1

    return render_template(
        "index.html",
        books=books,
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books,
        categories=categories,
        message="Category-wise Summary"
    )


# -------------------------
# RUN APPLICATION
# -------------------------

if __name__ == "__main__":
    create_file()
    app.run(debug=True)

