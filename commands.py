import sys
from datetime import datetime

import requests as rq

from database import DatabaseManager

db = DatabaseManager(db_name="bark.db")


class CreateBookmarksTableCommand:
    def execute(self) -> None:
        columns = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "title": "TEXT NOT NULL",
            "url": "TEXT NOT NULL",
            "notes": "TEXT",
            "date_added": "TEXT NOT NULL",
        }
        db.create_table("bookmarks", columns=columns)


class AddBookmarkCommand:
    def execute(self, data: dict[str, str], date_added: str | None = None) -> str:
        data["date_added"] = date_added or datetime.utcnow().isoformat()
        db.add("bookmarks", data)
        return "Bookmark added!"


class ListBookmarksCommand:
    def __init__(self, order_by: str = "date_added") -> None:
        self.order_by = order_by

    def execute(self) -> str:
        return "\n".join(
            str(bookmark)
            for bookmark in db.select("bookmarks", o_criteria=self.order_by).fetchall()
        )


class DeleteBookmarkCommand:
    def execute(self, id_b: int) -> str:
        db.delete("bookmarks", {"id": str(id_b)})
        return "Bookmark deleted!"


class EditBookmarkCommand:
    def execute(self, data: dict[str, str]) -> str:
        db.update("bookmarks", data)
        return "Bookmark updated!"


class ImportGithubStartsCommand:
    def execute(self, data: dict[str, str]) -> str:
        headers = {"Accept": "application/vnd.github.star+json"}
        url = f"https://api.github.com/users/{data['username']}/starred"
        command = AddBookmarkCommand()
        if data["time"].upper() == "Y":
            time = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
        else:
            time = lambda x: None

        num_imported = 0
        i = 1
        while bookmarks := rq.get(url=url, headers=headers, params={"page": i}).json():
            num_imported += len(bookmarks)
            for bookmark in bookmarks:
                command.execute(
                    data={
                        "title": bookmark["repo"]["name"],
                        "url": bookmark["repo"]["html_url"],
                        "notes": bookmark["repo"]["description"],
                    },
                    date_added=time(bookmark["starred_at"]),
                )
            i += 1
        return f"Imported {num_imported} bookmarks from starred repos!"


class QuitCommand:
    def execute(self) -> None:
        sys.exit()
