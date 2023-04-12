from abc import ABC, abstractmethod

from database import DatabaseManager


class PersistenceLayer(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError("Persistence layers must implement a create method")

    @abstractmethod
    def list_all(self, order_by):
        raise NotImplementedError("Persistence layers must implement a list_all method")

    @abstractmethod
    def edit(self, bookmark_id, data):
        raise NotImplementedError("Persistence layers must implement an edit method")

    @abstractmethod
    def delete(self, bookmark_id):
        raise NotImplementedError("Persistence layers must implement a delete method")


class BookmarkDatabase(PersistenceLayer):
    def __init__(self) -> None:
        self.table_name = "bookmarks"
        self.db = DatabaseManager(db_name="bark.db")

        columns = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "title": "TEXT NOT NULL",
            "url": "TEXT NOT NULL",
            "notes": "TEXT",
            "date_added": "TEXT NOT NULL",
        }
        self.db.create_table(self.table_name, columns=columns)

    def create(self, data):
        self.db.add(self.table_name, data)

    def list_all(self, order_by):
        return self.db.select(self.table_name, o_criteria=order_by).fetchall()

    def edit(self, bookmark_id, data):
        self.db.update(self.table_name, data)

    def delete(self, bookmark_id):
        self.db.delete(self.table_name, bookmark_id)
