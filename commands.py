import sys
from datetime import datetime

from database import DatabaseManager

db = DatabaseManager(db_name="bark.db")


class CreateBookmarksTableCommand:
    def execute(self):
        columns = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "title": "TEXT NOT NULL",
            "url": "TEXT NOT NULL",
            "notes": "TEXT",
            "date_added": "TEXT NOT NULL",
        }
        db.create_table("bookmarks", columns=columns)


class AddBookmarkCommand:
    def execute(self, data: dict[str, str]) -> str:
        data["date_added"] = datetime.utcnow().isoformat()
        db.add("bookmarks", data)
        return "Bookmark added!"


class ListBookmarksCommand:
    def __init__(self, order_by: str = "date_added") -> None:
        self.order_by = order_by

    def execute(self) -> list[str]:
        return db.select("bookmarks", o_criteria=self.order_by).fetchall()


class DeleteBookmarkCommand:
    def execute(self, id: int) -> str:
        db.delete("bookmarks", {"id": id})
        return "Bookmark deleted!"


class QuitCommand:
    def execute(self) -> None:
        sys.exit()
