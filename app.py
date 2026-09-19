import tkinter as tk

from database import Database
from ui import NotesApplication


def main():
    root = tk.Tk()

    database = Database()

    application = NotesApplication(
        root=root,
        database=database
    )

    root.protocol("WM_DELETE_WINDOW", application.close)
    root.mainloop()


if __name__ == "__main__":
    main()
