import readline
import os
import sys
from dataclasses import dataclass
from typing import List
from pickle import dumps, loads

FILE = "books.pkdb"
CLS = lambda: print("\033c\033[3J", end="")


@dataclass
class Book:
    title: str
    have_read: bool


@dataclass
class Series:
    name: str
    books: List[Book]


def check_db():
    if not os.path.isfile(FILE):
        with open(FILE, "wb") as f:
            f.write(
                dumps(
                    [
                        Series(
                            name="Inheritance",
                            books=[
                                Book(title="Eragon", have_read=True),
                                Book(title="Eldest", have_read=True),
                                Book(title="Brisingr", have_read=True),
                                Book(title="Inheritance", have_read=False),
                            ],
                        ),
                        Series(
                            name="Inheritance1",
                            books=[
                                Book(title="Eragon", have_read=True),
                                Book(title="Eldest", have_read=True),
                                Book(title="Brisingr", have_read=True),
                                Book(title="Inheritance", have_read=False),
                            ],
                        ),
                    ]
                )
            )


def read_text(book):
    return f'(Have {"" if book.have_read else "not "}read)'


def get_db():
    check_db()
    with open(FILE, "rb") as f:
        db = loads(f.read())
    return db


def set_db(db):
    check_db()
    with open(FILE, "wb") as f:
        f.write(dumps(db))


def edit_book(book):
    print("Book information")

    while True:
        read = input("Have read (y/n): ")
        if read in list("yn"):
            read = {"y": True, "n": False}[read]
            break
    book.have_read = read
    return book


def add_book():
    print("Book information")
    while True:
        title = input("Book title: ")
        if title:
            break

    while True:
        read = input("Have read (y/n): ")
        if read in list("yn"):
            read = {"y": True, "n": False}[read]
            break
    return Book(title, read)


def add_series():
    CLS()
    print("")
    print("******************************")
    print("***** Series information *****")
    print("******************************")
    print("")
    while True:
        name = input("Series name: ")
        if name:
            break
    books = []
    series = Series(name, books)
    return series


def book_menu(book):
    CLS()
    print("")
    print("***********************")
    print("*****  Book Menu  *****")
    print("***********************")
    print("")
    while True:
        print(book.title, read_text(book))
        print("b: go back")
        print("d: delete book")
        print("e: edit book")
        choice = ""
        while not choice:
            choice = input("Enter your choice: ")
        choice = choice.strip().lower()
        if choice == "b":
            return book
        elif choice == "e":
            book = edit_book(book)
        elif choice == "d":
            return None


def books_menu(series):
    CLS()
    print("")
    print("*************************")
    print("*****  Books Menu  *****")
    print("*************************")
    print("")
    while True:
        print(series.name)
        print("b: go back")
        print("d: delete series")
        print("n: new book")
        books = series.books
        for index, book in enumerate(books):
            print(f"{index}.", book.title, read_text(book))
        choice = ""
        while not choice:
            choice = input("Enter your choice: ")
        choice = choice.strip().lower()
        if choice == "b":
            series.books=books
            return series
        elif choice == "d":
            really = input("Are you *sure* (y/n)? ")
            if really == "y":
                return None
        elif choice == "n":
            books.append(add_book())
        elif choice.isdigit():
            number = int(choice)
            book = book_menu(books[number])
            if book:
                books[number] = book
            else:
                del books[number]


def series_menu():
    CLS()
    print("")
    print("*************************")
    print("*****  Series Menu  *****")
    print("*************************")
    print("")
    while True:
        print("b: go back")
        print("n: new series")
        db = get_db()
        for index, series in enumerate(db):
            print(f"{index}.", series.name)
        choice = ""
        while not choice:
            choice = input("Enter your choice: ")
        choice = choice.strip().lower()
        if choice == "b":
            return db
        elif choice == "n":
            series = add_series()
            db.append(series)
        elif choice.isdigit():
            number = int(choice)
            changed_series = books_menu(db[number])
            if changed_series:
                db[number] = changed_series
            else:
                del db[number]
        set_db(db)


def main_menu():
    CLS()
    print("")
    print("************************")
    print("*****  Main  Menu  *****")
    print("************************")
    print("")
    while True:
        print("q: quit BOOK-MGR")
        print("s: select series")
        print("l: list series with unread books")
        choice = ""
        while not choice:
            choice = input("Enter your choice: ")
        choice = choice.strip().lower()
        if choice == "q":
            sys.exit()
        elif choice == "s":
            series_menu()
        elif choice == "l":
            db = get_db()
            for series in db:
                print("")
                print(series.name + ":")
                for book in series.books:
                    if not book.have_read:
                        print("    " + book.title)

        print("")


def main():
    CLS()
    print("")
    print("██████╗░░█████╗░░█████╗░██╗░░██╗░░░░░░███╗░░░███╗░██████╗░██████╗░")
    print("██╔══██╗██╔══██╗██╔══██╗██║░██╔╝░░░░░░████╗░████║██╔════╝░██╔══██╗")
    print("██████╦╝██║░░██║██║░░██║█████═╝░█████╗██╔████╔██║██║░░██╗░██████╔╝")
    print("██╔══██╗██║░░██║██║░░██║██╔═██╗░╚════╝██║╚██╔╝██║██║░░╚██╗██╔══██╗")
    print("██████╦╝╚█████╔╝╚█████╔╝██║░╚██╗░░░░░░██║░╚═╝░██║╚██████╔╝██║░░██║")
    print("╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝░░░░░░╚═╝░░░░░╚═╝░╚═════╝░╚═╝░░╚═╝")
    print("")
    print("")
    input("Press Enter to continue... ")
    main_menu()


main()
