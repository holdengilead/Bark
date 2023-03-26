import sqlite3


class DatabaseManager:
    def __init__(self, db_name: str) -> None:
        self.connection = sqlite3.connect(db_name)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values: list[str] = None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, name: str, columns: dict[str, str]):
        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ]
        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {name} (
                {','.join(columns_with_types)}
            ); 
            """
        )

    def add(self, table_name: str, data: dict[str]) -> None:
        placeholder = ", ".join("?" * len(data))
        column_names = f"({', '.join(data.keys())})"
        self._execute(
            f"""
            INSERT INTO {table_name}
            {column_names}
            VALUES ({placeholder});
            """,
            values=tuple(data.values()),
        )

    def delete(self, table_name: str, columns: dict[str, str]) -> None:
        placeholders = (f"{column} = ?" for column in columns)
        criteria = " AND ".join(placeholders)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {criteria};
            """,
            tuple(columns.values()),
        )

    def select(
        self, table_name: str, columns: dict[str, str] = None, o_criteria: str = None
    ) -> sqlite3.Cursor:
        columns = columns or {}

        placeholders = (f"{column} = ?" for column in columns.items())
        s_criteria = " AND ".join(placeholders)
        select_criteria = f"WHERE {s_criteria}" if columns else ""
        order_criteria = f"ORDER BY {o_criteria}" if o_criteria else ""
        return self._execute(
            f"""
            SELECT * FROM {table_name}
            {select_criteria}
            {order_criteria};
            """,
            tuple(columns.values()),
        )
