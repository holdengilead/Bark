import os

import commands


class Option:
    def __init__(self, name, command, prep_call=None) -> None:
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self) -> str:
        return self.name


def print_options(options: dict[str, Option]):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def get_user_choice(options):
    choice = input("Choose an option: ")
    while choice.upper() not in options:
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label} :") or None
    return value


def get_info_new_bookmark():
    return {
        "title": get_user_input("title"),
        "url": get_user_input("url"),
        "notes": get_user_input("notes", required=False),
    }


def get_id_to_delete():
    return int(get_user_input("id"))


def loop(options):
    os.system("clear")
    print_options(options)
    user_choice = get_user_choice(options)
    os.system("clear")
    user_choice.choose()
    input("Press ENTER to return to menu")


if __name__ == "__main__":
    commands.CreateBookmarksTableCommand().execute()
    options = {
        "A": Option(
            name="Add a bookmark",
            command=commands.AddBookmarkCommand(),
            prep_call=get_info_new_bookmark,
        ),
        "B": Option(
            name="List bookmarks by date", command=commands.ListBookmarksCommand()
        ),
        "T": Option(
            name="List bookmarks by title",
            command=commands.ListBookmarksCommand(order_by="title"),
        ),
        "D": Option(
            name="Delete a bookmark",
            command=commands.DeleteBookmarkCommand(),
            prep_call=get_id_to_delete,
        ),
        "Q": Option(name="Quit", command=commands.QuitCommand()),
    }

    while True:
        loop(options)
