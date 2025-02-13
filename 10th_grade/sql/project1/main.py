from tabulate import tabulate

from db.models import Database


cache = {}


def welcome():
    print("welcome!\nInstruction:...")


def get_acceptation(text: str) -> bool:
    acceptation = input(f"{text} [Y]es|[No]: ")
    if acceptation.lower() not in ("yes", "y", ""):
        print("Operation was successfully canceled.")
        return False
    return True


def check_signed_in() -> bool:
    return "user" in cache


def main():
    db_path = "./tasks.db"
    db = Database(db_path)

    welcome()

    while user_input := input():
        args = user_input.split()
        match args[0]:
            case "sign-up" | "su":
                acceptation = get_acceptation("You want to create a new account?")
                if not acceptation:
                    continue

                name = input("Your name: ")
                surname = input("Your surname: ")
                patronymic = input("Your patronymic (in the absence, just click on enter): ")
                patronymic = patronymic if patronymic else None
                license_id = input("Your license-id: ")
                address = input("And finally your address: ")
            case "sign-in" | "si":
                acceptation = get_acceptation("You want sing in your account?")
                if not acceptation:
                    continue

                license_id = input("Your license-id: ")
                found_users = db.users.search()
                if len(found_users) == 0:
                    print(f"No user with license-id \"{license_id}\"")
                else:
                    user = found_users[0]
                    cache["user"] = user

            case "relocate" | "rl":
                is_signed_in = check_signed_in()
                if not is_signed_in:
                    print("Firstly sign in (user command si).")
                    continue

                acceptation = get_acceptation("You want to change your address?")
                if not acceptation:
                    continue

                new_address = input("Your new address: ")
                user_id = cache["user"][0]
                old_address = cache["user"][5]
                db.users.relocate(user_id, new_address)
                cache[5] = new_address

                print(f"Address successfully updated: {old_address} ⟶ {new_address}.")

            case "find" | "search" | "f" | "s":
                pattern = input("Enter your request: ")
                books = db.books.search(pattern)
                if len(books) == 0:
                    print("No books found for your search.")
                else:
                    print(tabulate(books, headers=['Id', 'Name', 'Author', 'Pub. year', 'Edition', 'Wardrobe №', 'Shelf №'], tablefmt='rounded_grid'))

            case "borrow" | "br":
                is_signed_in = check_signed_in()
                if not is_signed_in:
                    print("Firstly sign in (use command si).")
                    continue

                acceptation = get_acceptation("You want to borrow a book?")
                if not acceptation:
                    continue
                
                book_id = input("Book-id (to find out the book-id use command \"s\"):")
                if len(book_id) == 0:
                    print("Borrowing a book is canceled.")
                elif not db.books.check_book_exists(book_id):
                    print("Book by this id does not exist.")
                elif not db.books.check_book_is_free(book_id):
                    print("Book by this id has already been borrowed.")
                else:
                    user_id = cache["user"][0]
                    db.books.borrow(book_id, user_id)
                    print("Book is successfully borrowed.")
            
            case "take-back" | "return" | "rt" | "tk":
                is_signed_in = check_signed_in()
                if not is_signed_in:
                    print("Firstly sign in (use command \"si\").")
                    continue

                acceptation = get_acceptation("You want to borrow a book?")
                if not acceptation:
                    continue
                
                user_id = cache["user"][0]
                books = db.users.get_borrowed_books(user_id)
                if len(books) == 0:
                    print("You have not borrowed any books.")
                    continue
                
                print("Books borrowed by you:")
                print(tabulate(books, headers=['Id', 'Name', 'Author', 'Edition', 'Pub. year'], tablefmt='rounded_grid'))
                book_id = input("Book-id you want to take back: ")
                book_id_list = [book[0] for book in books]
                if book_id not in book_id_list:
                    print("There is no book by this id.")
                else:
                    db.books.take_back(book_id)
                    print("Book is successfully taken back.")


            case "quit" | "q" | "exit":
                break

            case _:
                raise ValueError("invalid command-line argument")


if __name__ == "__main__":
    main()

