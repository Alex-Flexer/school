import sqlite3

from db.utils import get_script_from_file


class Database:
    """
    Class for database interaction
    """

    class Books:
        """
        Class implementing task table logic
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

        def all(self) -> list[tuple[str, str, bool]]:
            return self._template_query("all.sql")

        def add(self, *book_details) -> None:
            """
            book_details: (name, author, pub_yer, editioon, wardrobe_id, shelf_id )
            """
            self._template_query("add.sql", *book_details)

        def delete(self, id: int) -> None:
            self._template_query("delete.sql", id)

        def search(self, pattern: str) -> list[tuple[int, str, str, bool]]:
            return self._template_query("search.sql", pattern, pattern)

        def borrow(self, book_id: int, user_id) -> None:
            self._template_query("borrow.sql", book_id, user_id)
        
        def take_back(self, book_id: int, user_id: int) -> None:
            self._template_query("take_back.sql", book_id, user_id)

        
    class Users:
        """
        Class implementing task table logic
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

        def create(self, *user_details) -> None:
            """
            book_details: (name, author, pub_yer, editioon, wardrobe_id, shelf_id )
            """
            self._template_query("create.sql", *user_details)

        def delete(self, id: int) -> None:
            self._template_query("delete.sql", id)

        def search(self, pattern: str) -> list[tuple[int, str, str, bool]]:
            return self._template_query("search.sql", pattern, pattern)
    
    conn : sqlite3.Connection
    books: Books
    users: Users

    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.executescript(get_script_from_file("db_init.sql"))
        self.conn.commit()

        self.books = Database.Books(self.conn)
        self.users = Database.Users(self.conn)

