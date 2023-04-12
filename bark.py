import os
from typing import Callable

import commands

# TO-DO: Arreglar el choose. Ya no hace falta el if / else en message = ...


class Option:
    def __init__(
        self,
        name: str,
        command: commands.Command,
        message: str,
        prep_call: Callable[[], dict[str, str]] | None = None,
    ) -> None:
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.message = message

    def choose(self) -> None:
        data = self.prep_call() if self.prep_call else None
        _, result = self.command.execute(data) if data else self.command.execute()
        if result:
            print(result)
        if self.message:
            print(self.message)

    def __str__(self) -> str:
        return self.name


def print_options(options: dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def get_user_choice(options: dict[str, Option]) -> Option:
    choice = input("Choose an option: ")
    while choice.upper() not in options:
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label: str, required: bool = True) -> str:
    value = input(f"{label}: ")
    while required and not value:
        value = input(f"{label} :")
    return value


def get_github_import_options() -> dict[str, str]:
    return {
        "username": get_user_input("GitHub username"),
        "time": get_user_input("Preserve timestamps [Y/n]"),
    }


def get_info_new_bookmark() -> dict[str, str]:
    return {
        "title": get_user_input("title"),
        "url": get_user_input("url"),
        "notes": get_user_input("notes", required=False),
    }


def get_info_update() -> dict[str, str]:
    return {
        "id": get_user_input("Bookmark ID"),
        "columns": get_user_input("Field name"),
        "new_value": get_user_input("New value"),
    }


def get_id_to_delete() -> dict[str, str]:
    return {"id": get_user_input("id")}


def loop(options: dict[str, Option]) -> None:
    os.system("clear")
    print_options(options)
    user_choice = get_user_choice(options)
    os.system("clear")
    user_choice.choose()
    input("\nPress ENTER to return to menu")


if __name__ == "__main__":
    # commands.CreateBookmarksTableCommand().execute()
    options: dict[str, Option] = {
        "A": Option(
            name="Add a bookmark",
            command=commands.AddBookmarkCommand(),
            prep_call=get_info_new_bookmark,
            message="Bookmark added!",
        ),
        "B": Option(
            name="List bookmarks by date",
            command=commands.ListBookmarksCommand(),
            message="",
        ),
        "T": Option(
            name="List bookmarks by title",
            command=commands.ListBookmarksCommand(order_by="title"),
            message="",
        ),
        "D": Option(
            name="Delete a bookmark",
            command=commands.DeleteBookmarkCommand(),
            prep_call=get_id_to_delete,
            message="Bookmark deleted!",
        ),
        "G": Option(
            name="Import GitHub stars",
            command=commands.ImportGithubStartsCommand(),
            prep_call=get_github_import_options,
            message="",
        ),
        "E": Option(
            name="Update a bookmark",
            command=commands.EditBookmarkCommand(),
            prep_call=get_info_update,
            message="Bookmark updated!",
        ),
        "Q": Option(name="Quit", command=commands.QuitCommand(), message=""),
    }

    while True:
        loop(options)
