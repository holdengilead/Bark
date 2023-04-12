import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable

import requests as rq

from persistence import BookmarkDatabase

db = BookmarkDatabase()

# TO-DO: Crear un TypedDict (creo que mejor un dataclass) con todos los campos a
# recibir. Así, data siempre va a ser de ese tipo, y nunca None, evitando muchos fallos
# de MyPy. Las funciones prep_call instancian un nuevo objeto de ese tipo, con valores
# por defecto nulos, y cambian los valores para el comando correspondiente.


class Command(ABC):
    @abstractmethod
    def execute(self, data: dict[str, str] | None = None) -> str:
        raise NotImplementedError


class AddBookmarkCommand(Command):
    def execute(self, data: dict[str, str] | None = None) -> str:
        if "date_added" not in data or data["date_added"] == "":
            data["date_added"] = datetime.utcnow().isoformat()
        db.create(data)
        return True, None


class ListBookmarksCommand(Command):
    def __init__(self, order_by: str = "date_added") -> None:
        super().__init__()
        self.order_by = order_by

    def execute(self, data: dict[str, str] | None = None) -> str:
        return True, "\n".join(str(bookmark) for bookmark in db.list_all(self.order_by))


class DeleteBookmarkCommand(Command):
    def execute(self, data: dict[str, str] | None = None) -> str:
        db.delete(data)
        return True, None


class EditBookmarkCommand(Command):
    def execute(self, data: dict[str, str] | None = None) -> str:
        db.edit(data["id"], data)
        return True, None


class ImportGithubStartsCommand(Command):
    def execute(self, data: dict[str, str] | None = None) -> str:
        headers = {"Accept": "application/vnd.github.star+json"}
        url = f"https://api.github.com/users/{data['username']}/starred"
        command = AddBookmarkCommand()
        time: Callable[[str], str]
        if data["time"].upper() == "Y":
            time = lambda x: str(datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
        else:
            time = lambda x: ""

        num_imported = 0
        i = 1
        while bookmarks := rq.get(url=url, headers=headers, params={"page": i}).json():
            num_imported += len(bookmarks)
            for bookmark in bookmarks:
                command.execute(
                    {
                        "title": bookmark["repo"]["name"],
                        "url": bookmark["repo"]["html_url"],
                        "notes": bookmark["repo"]["description"],
                        "date_added": time(bookmark["starred_at"]),
                    }
                )
            i += 1
        return True, f"Imported {num_imported} bookmarks from starred repos!"


class QuitCommand(Command):
    def execute(self, data: dict[str, str] | None = None) -> str:
        sys.exit()
