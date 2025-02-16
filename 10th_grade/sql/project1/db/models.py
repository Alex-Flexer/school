"""Module providing a function printing python version."""
import sqlite3
from db.utils import get_script_from_file


class Database:
    """
    Class for database interaction
    """

    class Books:
        """
        Class implementing books table logic
        """

        conn: sqlite3.Connection

        def __init__(self, conn: sqlite3.Connection) -> None:
            self.conn = conn

        def _template_query(self, script: str, *args) -> list[tuple]:
            cursor = self.conn.cursor()
            script = get_script_from_file(f"books/{script}")
            res = cursor.execute(script, args)
            self.conn.commit()
            return res.fetchall()

        def all(self) -> list[tuple[str]]:
            """
            Method return all book
            """
            return self._template_query("all.sql")

        def all_free(self) -> list[tuple[str]]:
            """
            Method return all free book
            """
            return self._template_query("all_free.sql")

        def add(self, *book_details) -> None:
            """
            book_details: (name, author, pub_yer, edition, wardrobe_id, shelf_id )
            """
            self._template_query("add.sql", *book_details)

        def search(self, pattern: str) -> list[tuple[int, str, str, bool]]:
            """
            Method provides searching a book by pattern
            """
            return self._template_query("search.sql", pattern, pattern)

        def borrow(self, book_id: int, user_id) -> None:
            """
            Method provides borrowing a book
            """
            self._template_query("borrow.sql", book_id, user_id)

        def check_book_exists(self, book_id) -> bool:
            """
            Method provides checking existence of book
            """
            return len(self._template_query("get.sql", book_id)) > 0

        def check_book_is_free(self, book_id) -> bool:
            """
            Method provides checking is book free
            """
            return len(self._template_query("get_borrower_book_conn.sql", book_id)) == 0

        def take_back(self, book_id: int) -> None:
            """
            Method provides taking back a book
            """
            self._template_query("take_back.sql", book_id)

        def check_place_free(self, wardrobe_id, shelf_id) -> bool:
            """
            Method provides checking emptiness 
            """
            books = self._template_query(
                "books_in_certain_place.sql",
                shelf_id, wardrobe_id
            )
            return len(books) == 0

        def move(self,
                 wardrobe_id: str,
                 shelf_id: str,
                 new_wardrobe_id: str,
                 new_shelf_id: str
                 ) -> None:
            """
            Method provides moving a book
            """
            return self._template_query(
                "move.sql",
                new_wardrobe_id, new_shelf_id, wardrobe_id, shelf_id
            )

    class Users:
        """
        Class implementing users table logic
        """

        conn: sqlite3.Connection

        def __init__(self, conn: sqlite3.Connection) -> None:
            self.conn = conn

        def _template_query(self, script: str, *args) -> list[tuple]:
            cursor = self.conn.cursor()
            script = get_script_from_file(f"users/{script}")
            res = cursor.execute(script, args)
            self.conn.commit()
            return res.fetchall()

        def all(self) -> list[tuple[str]]:
            """
            Method return all users
            """
            return self._template_query("all.sql")

        def create(self, *user_details) -> None:
            """
            book_details: (name, surname, patronymic, license-id, address)
            """
            self._template_query("add.sql", *user_details)

        def delete(self, license_id: str) -> None:
            """
            Method deletes user
            """
            self._template_query("delete.sql", license_id)

        def search(self, license_id: str) -> list[tuple[int, str, str, bool]]:
            """
            Method provides searching a user
            """
            return self._template_query("search.sql", license_id)

        def relocate(self, user_id, new_address: str) -> None:
            """
            Method provides changing an address 
            """
            self._template_query("relocate.sql", new_address, user_id)

        def get_borrowed_books(self, user_id) -> list[tuple[str]]:
            """
            Method return all borrowed books by certain user 
            """
            return self._template_query("get_borrowed_books.sql", user_id)

    conn: sqlite3.Connection
    books: Books
    users: Users

    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.executescript(get_script_from_file("db_init.sql"))
        self.conn.commit()

        self.books = Database.Books(self.conn)
        self.users = Database.Users(self.conn)
