"""Module provides beautiful printing tables"""
import os
import difflib
from tabulate import tabulate
from db.models import Database


cache = {}
COMMANDS = [
    "all", "a", "all-free", "af", "quit",
    "find-user", "fu", "search", "find", "exit",
    "s", "f", "my", "help", "h", "sign-in", "q",
    "si", "sign-up", "su", "delete", "del", "d",
    "delete-user", "del-user", "du", "borrow",
    "br", "take-back", "tb", "relocate", "rl",
    "move", "mv", "add", "create", "cr", "remove", "rm"
]


def welcome():
    """
    Function print welcome
    """
    print("Welcome to Flexer-Lib-System!\n"
          "To get instruction use \"help\" (h)\n\n")


def pprint(*args, **kwargs):
    """
    Function provides printing with clearing
    """
    os.system("cls")
    print(*args, **kwargs)


def get_acceptation(text: str) -> bool:
    """
    Function checks acceptation from user
    """
    acceptation = input(f"{text} [Y]es|[N]o: ")
    if acceptation.lower() not in ("yes", "y", ""):
        print("Operation was successfully canceled.")
        return False
    return True


def check_signed_in() -> bool:
    """
    Function check is user signed in
    """
    return "user" in cache


def main():
    """
    Just main
    """
    db_path = "./lib.db"
    db = Database(db_path)

    welcome()

    while user_input := input(">>> "):
        pprint(end="")
        cmd = user_input
        match cmd:
            case "sign-up" | "su":
                acceptation = get_acceptation(
                    "You want to create a new account?")
                if not acceptation:
                    continue

                name = input("User's name: ")
                surname = input("User's surname: ")
                patronymic = input(
                    "User's patronymic (optional): ")
                patronymic = patronymic if patronymic else None
                license_id = input("User's license-id: ")
                address = input("And finally user's address (optional): ")
                if len(db.users.search(license_id)) == 0:
                    try:
                        db.users.create(
                            name,
                            surname,
                            patronymic,
                            license_id,
                            address
                        )
                    except Exception as e:
                        pprint(f"ERROR: {e}")
                    else:
                        pprint("Users is successfully created.")
                else:
                    pprint("User with this license-id already exists.")

            case "sign-in" | "si":
                acceptation = get_acceptation("You want sing in your account?")
                if not acceptation:
                    continue

                license_id = input("Your license-id: ")
                found_users = db.users.search(license_id)
                if len(found_users) == 0:
                    pprint(f"No user with license-id \"{license_id}\"")
                else:
                    user = found_users[0]
                    cache["user"] = user
                    pprint(
                        "You are successfully signed in."
                        f"Your current license-id: {license_id}"
                    )

            case "my":
                is_signed_in = check_signed_in()
                if not is_signed_in:
                    pprint("Firstly sign in (user command si).")
                    continue

                user_id = user[0]
                books = db.users.get_borrowed_books(user_id)
                if len(books) == 0:
                    pprint("You have not borrowed any books yet.")
                else:
                    pprint("Books borrowed by user:")
                    print(tabulate(
                        books,
                        headers=['Id', 'Name', 'Author',
                                 'Edition', 'Pub. year'],
                        tablefmt='rounded_grid')
                    )

            case "relocate" | "rl":
                is_signed_in = check_signed_in()
                if not is_signed_in:
                    pprint("Firstly sign in (user command si).")
                    continue

                acceptation = get_acceptation(
                    "You want to change your address?")
                if not acceptation:
                    continue

                new_address = input("Your new address: ")
                user_id = cache["user"][0]
                old_address = cache["user"][5]
                try:
                    db.users.relocate(user_id, new_address)
                except Exception as e:
                    pprint(f"ERROR: {e}")
                else:
                    cache[5] = new_address
                    pprint(
                        "Address successfully updated:"
                        f"{old_address} ⟶ {new_address}."
                    )

            case "del-user" | "delete-user" | "del-u" | "du":
                license_id = input("User's license-id: ")
                if len(db.users.search(license_id)) > 0:
                    try:
                        db.users.delete(license_id)
                    except Exception as e:
                        pprint(f"ERROR: {e}")
                    else:
                        pprint("User is successfully deleted.")
                else:
                    pprint("There is no user with this license-id.")

            case "find" | "search" | "f" | "s":
                pattern = input("Enter your request: ")
                books = db.books.search(pattern)
                if len(books) == 0:
                    pprint("No books found for your search.")
                else:
                    pprint(tabulate(
                        books,
                        headers=['Id', 'Name', 'Author', 'Pub. year',
                                 'Edition', 'Wardrobe №', 'Shelf №'],
                        tablefmt='rounded_grid')
                    )
            case "fu" | "find-user":
                license_id = input("Users's license-id: ")
                pprint(db.users.search(license_id),)
                pprint(tabulate(
                    db.users.search(license_id),
                    headers=['Name', 'Surname', 'Patronymic', "License-id", 'Address'],
                    tablefmt='rounded_grid')
                )

            case "borrow" | "br":
                is_signed_in = check_signed_in()
                if not is_signed_in:
                    pprint("Firstly sign in (use command si).")
                    continue

                acceptation = get_acceptation("You want to borrow a book?")
                if not acceptation:
                    continue

                book_id = input(
                    "Book-id (to find out the book-id use command \"s\"): ")
                if len(book_id) == 0:
                    pprint("Borrowing a book is canceled.")
                elif not db.books.check_book_exists(book_id):
                    pprint("Book by this id does not exist.")
                elif not db.books.check_book_is_free(book_id):
                    pprint("Book by this id has already been borrowed.")
                else:
                    user_id = cache["user"][0]
                    try:
                        db.books.borrow(book_id, user_id)
                    except Exception as e:
                        pprint(f"ERROR: {e}")
                    else:
                        pprint("Book is successfully borrowed.")

            case "take-back" | "return" | "rt" | "tb":
                is_signed_in = check_signed_in()
                if not is_signed_in:
                    pprint("Firstly sign in (use command \"si\").")
                    continue

                acceptation = get_acceptation("You want to borrow a book?")
                if not acceptation:
                    continue

                user_id = cache["user"][0]
                books = db.users.get_borrowed_books(user_id)
                if len(books) == 0:
                    pprint("You have not borrowed any books.")
                    continue

                pprint("Books borrowed by you:")
                print(tabulate(books, headers=[
                      'Id', 'Name', 'Author', 'Edition', 'Pub. year'], tablefmt='rounded_grid'))
                while not (book_id := input("Book-id you want to take back: ")).isdecimal():
                    print("Book-id must be integer, try again.")

                book_id_list = [book[0] for book in books]
                if int(book_id) not in book_id_list:
                    pprint(f"There is no book by id \"{book_id}\".")
                else:
                    try:
                        db.books.take_back(book_id)
                    except Exception as e:
                        pprint(f"ERROR: {e}")
                    else:
                        pprint("Book is successfully taken back.")

            case "add" | "create" | "cr":
                name = input("Name of new book: ")
                author = input("Book's author: ")
                while not (pub_year := input("When was it published: ")).isdecimal():
                    print("Year must be integer, try again.")

                edition = input("What's edition: ")

                while not (wardrobe_id := input("Wardrobe index: ")).isdecimal():
                    print("Wardrobe index must be integer, try again.")

                while not (shelf_id := input("Shelf's index: ")).isdecimal():
                    print("Shelf index must be integer, try again.")

                if not db.books.check_place_free(wardrobe_id, shelf_id):
                    pprint("This place is busy.")
                else:
                    db.books.add(
                        name,
                        author,
                        pub_year,
                        edition,
                        wardrobe_id,
                        shelf_id
                    )

            case "delete" | "del" | "d" | "remove" | "rm":
                book_id = input("Book-id: ")
                if not db.books.check_book_exists(book_id):
                    pprint("Book by this id does not exist.")
                else:
                    db.books.add(book_id)

            case "move" | "mv":
                while not (wardrobe_id := input("Wardrobe index: ")).isdecimal():
                    print("Wardrobe index must be integer, try again.")

                while not (shelf_id := input("Shelf's index: ")).isdecimal():
                    print("Shelf index must be integer, try again.")

                if db.books.check_place_free(wardrobe_id, shelf_id):
                    pprint("There is no book on this place.")
                    continue

                while not (new_wardrobe_id := input("New wardrobe index: ")).isdecimal():
                    print("Wardrobe index must be integer, try again.")

                while not (new_shelf_id := input("New shelf's index: ")).isdecimal():
                    print("Shelf index must be integer, try again.")

                if not db.books.check_place_free(new_wardrobe_id, new_shelf_id):
                    pprint("This place is busy.")
                else:
                    try:
                        db.books.move(
                            wardrobe_id,
                            shelf_id,
                            new_wardrobe_id,
                            new_shelf_id
                        )
                    except Exception as e:
                        pprint(f"ERROR: {e}")
                    else:
                        pprint("Position of book is successfully changed.")

            case "all" | "a":
                books = db.books.all()
                pprint(tabulate(
                    books, headers=['Id', 'Name', 'Author',
                                    'Pub. year', 'Edition', 'Wardrobe №', 'Shelf №'],
                    tablefmt='rounded_grid')
                )

            case "all-free" | "af":
                books = db.books.all_free()
                pprint(tabulate(
                    books,
                    headers=['Id', 'Name', 'Author', 'Pub. year',
                             'Edition', 'Wardrobe №', 'Shelf №'],
                    tablefmt='rounded_grid')
                )

            case "help" | "h":
                print(
                    "Instruction:\n\n\n"
                    "all (a) - get all books\n\n"
                    "all-free (af) - get all free books\n\n"
                    "search/find (s/f) - find a book by pattern\n\n"
                    "add/create (cr) - add the book to database\n\n"
                    "delete/remove (del/rm) - remove book from database\n\n"
                    "move (mv) - change position of the book\n\n"
                    "sign-up (su) - create an account of user\n\n"
                    "sign-in (si) - sign in the user's account\n\n"
                    "find-user (fu) - find user by license-id\n\n"
                    "delete-user (du) - delete user by license-id\n\n"
                    "borrow (br) - borrow a book for user\n\n"
                    "take-back (tb) - take back a book\n\n"
                    "relocate (rl) - change an address of user\n\n"
                    "help (h) - get help manual"
                )

            case "quit" | "q" | "exit":
                break

            case _:
                sim_cmd = difflib.get_close_matches(cmd, COMMANDS)
                pprint(f"Unknown command \"{cmd}\".")
                if len(sim_cmd) > 0:
                    print("Probably you meant:", ", ".join(sim_cmd))


if __name__ == "__main__":
    main()
