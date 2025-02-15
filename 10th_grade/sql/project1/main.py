"""Module provides beautiful printing tables"""
from tabulate import tabulate
import os
from db.models import Database


cache = {}


def welcome():
    """
    Function print welcome 
    """
    print("Welcome to Flexer-Lib-System!\n\n")

def pprint(*args, **kwargs):
    """
    Function provides printing with clearing
    """
    os.system("clear")
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
        pprint()
        cmd = user_input
        match cmd:
            case "sign-up" | "su":
                acceptation = get_acceptation(
                    "You want to create a new account?")
                if not acceptation:
                    continue

                name = input("Your name: ")
                surname = input("Your surname: ")
                patronymic = input(
                    "Your patronymic (in the absence, just click on enter): ")
                patronymic = patronymic if patronymic else None
                license_id = input("Your license-id: ")
                address = input("And finally your address: ")
                if len(db.users.search(license_id)) == 0:
                    db.users.create(name, surname, patronymic,
                                    license_id, address)
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
                db.users.relocate(user_id, new_address)
                cache[5] = new_address

                pprint(
                    f"Address successfully updated: {old_address} ⟶ {new_address}.")

            case "del-user" | "delete-user" | "del-u" | "du":
                license_id = input("User's license-id: ")
                if len(db.users.search(license_id)) > 0:
                    db.users.delete(license_id)
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
                print(db.users.search(license_id))

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
                    db.books.borrow(book_id, user_id)
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
                    db.books.take_back(book_id)
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

                db.books.add(name, author, pub_year,
                             edition, wardrobe_id, shelf_id)

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
                    db.books.move(wardrobe_id, shelf_id,
                                  new_wardrobe_id, new_shelf_id)

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

            case "quit" | "q" | "exit":
                break

            case _:
                raise ValueError("invalid command-line argument")


if __name__ == "__main__":
    main()
