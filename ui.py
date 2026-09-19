import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from config import (
    APP_NAME,
    APP_VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MAX_NOTE_TITLE_LENGTH
)


class NotesApplication:

    def __init__(
        self,
        root,
        database
    ):

        self.root = root
        self.database = database

        self.current_user = None
        self.current_note_id = None

        self.configure_root()

        self.show_login_screen()

    # =========================================================
    # WINDOW
    # =========================================================

    def configure_root(self):

        self.root.title(
            "{} {}".format(
                APP_NAME,
                APP_VERSION
            )
        )

        self.root.geometry(
            "{}x{}".format(
                WINDOW_WIDTH,
                WINDOW_HEIGHT
            )
        )

        self.root.minsize(
            900,
            600
        )

        self.root.configure(
            bg="#eef2f7"
        )

        self.setup_styles()

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 15, "bold")
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.configure(
            "TButton",
            padding=7
        )

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # =========================================================
    # LOGIN
    # =========================================================

    def show_login_screen(self):

        self.clear_window()

        container = tk.Frame(
            self.root,
            bg="#eef2f7"
        )

        container.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            container,
            bg="white",
            padx=45,
            pady=40,
            bd=1,
            relief="solid"
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        title = tk.Label(
            card,
            text=APP_NAME,
            bg="white",
            fg="#172033",
            font=("Segoe UI", 25, "bold")
        )

        title.pack(
            pady=(0, 5)
        )

        subtitle = tk.Label(
            card,
            text="Secure personal notes",
            bg="white",
            fg="#667085",
            font=("Segoe UI", 11)
        )

        subtitle.pack(
            pady=(0, 30)
        )

        tk.Label(
            card,
            text="Username",
            bg="white",
            fg="#344054",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.login_username = tk.Entry(
            card,
            width=35,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )

        self.login_username.pack(
            pady=(6, 15),
            ipady=7
        )

        tk.Label(
            card,
            text="Password",
            bg="white",
            fg="#344054",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.login_password = tk.Entry(
            card,
            width=35,
            font=("Segoe UI", 11),
            show="*",
            relief="solid",
            bd=1
        )

        self.login_password.pack(
            pady=(6, 20),
            ipady=7
        )

        login_button = tk.Button(
            card,
            text="LOGIN",
            command=self.login,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=31
        )

        login_button.pack(
            pady=(0, 10),
            ipady=8
        )

        register_button = tk.Button(
            card,
            text="CREATE NEW ACCOUNT",
            command=self.show_register_screen,
            bg="white",
            fg="#2563eb",
            activebackground="white",
            activeforeground="#1d4ed8",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )

        register_button.pack()

        self.login_password.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.login_username.focus_set()

    # =========================================================
    # REGISTER
    # =========================================================

    def show_register_screen(self):

        self.clear_window()

        container = tk.Frame(
            self.root,
            bg="#eef2f7"
        )

        container.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            container,
            bg="white",
            padx=45,
            pady=35,
            bd=1,
            relief="solid"
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            card,
            text="Create Account",
            bg="white",
            fg="#172033",
            font=("Segoe UI", 24, "bold")
        ).pack(
            pady=(0, 6)
        )

        tk.Label(
            card,
            text="Your account and notes remain saved on this PC.",
            bg="white",
            fg="#667085",
            font=("Segoe UI", 10)
        ).pack(
            pady=(0, 25)
        )

        tk.Label(
            card,
            text="Username",
            bg="white",
            fg="#344054",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.register_username = tk.Entry(
            card,
            width=35,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )

        self.register_username.pack(
            pady=(6, 15),
            ipady=7
        )

        tk.Label(
            card,
            text="Password",
            bg="white",
            fg="#344054",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.register_password = tk.Entry(
            card,
            width=35,
            font=("Segoe UI", 11),
            show="*",
            relief="solid",
            bd=1
        )

        self.register_password.pack(
            pady=(6, 15),
            ipady=7
        )

        tk.Label(
            card,
            text="Confirm Password",
            bg="white",
            fg="#344054",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.register_confirm = tk.Entry(
            card,
            width=35,
            font=("Segoe UI", 11),
            show="*",
            relief="solid",
            bd=1
        )

        self.register_confirm.pack(
            pady=(6, 20),
            ipady=7
        )

        tk.Button(
            card,
            text="CREATE ACCOUNT",
            command=self.register,
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=31
        ).pack(
            pady=(0, 10),
            ipady=8
        )

        tk.Button(
            card,
            text="BACK TO LOGIN",
            command=self.show_login_screen,
            bg="white",
            fg="#2563eb",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack()

        self.register_username.focus_set()

    def register(self):

        username = self.register_username.get().strip()
        password = self.register_password.get()
        confirmation = self.register_confirm.get()

        if not username:
            messagebox.showerror(
                "Registration",
                "Please enter a username."
            )
            return

        if len(username) > 50:
            messagebox.showerror(
                "Registration",
                "Username must not exceed 50 characters."
            )
            return

        if len(password) < 6:
            messagebox.showerror(
                "Registration",
                "Password must contain at least 6 characters."
            )
            return

        if password != confirmation:
            messagebox.showerror(
                "Registration",
                "Passwords do not match."
            )
            return

        success, message = self.database.register_user(
            username,
            password
        )

        if not success:

            messagebox.showerror(
                "Registration",
                message
            )

            return

        messagebox.showinfo(
            "Registration",
            "Account created successfully.\n\nYou can now log in."
        )

        self.show_login_screen()

        self.login_username.insert(
            0,
            username
        )

        self.login_password.focus_set()

    # =========================================================
    # LOGIN ACTION
    # =========================================================

    def login(self):

        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:

            messagebox.showwarning(
                "Login",
                "Please enter your username and password."
            )

            return

        user = self.database.login_user(
            username,
            password
        )

        if user is None:

            messagebox.showerror(
                "Login",
                "Invalid username or password."
            )

            return

        self.current_user = user

        self.show_main_screen()

    # =========================================================
    # MAIN SCREEN
    # =========================================================

    def show_main_screen(self):

        self.clear_window()

        main = tk.Frame(
            self.root,
            bg="#eef2f7"
        )

        main.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # TOP BAR
        # -----------------------------------------------------

        top = tk.Frame(
            main,
            bg="#172033",
            height=65
        )

        top.pack(
            fill="x"
        )

        tk.Label(
            top,
            text=APP_NAME,
            bg="#172033",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(
            side="left",
            padx=20
        )

        user_frame = tk.Frame(
            top,
            bg="#172033"
        )

        user_frame.pack(
            side="right",
            padx=15
        )

        tk.Label(
            user_frame,
            text="Logged in: {}".format(
                self.current_user["username"]
            ),
            bg="#172033",
            fg="#d0d5dd",
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            padx=(0, 15)
        )

        tk.Button(
            user_frame,
            text="LOGOUT",
            command=self.logout,
            bg="#344054",
            fg="white",
            activebackground="#475467",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="left"
        )

        # -----------------------------------------------------
        # BODY
        # -----------------------------------------------------

        body = tk.Frame(
            main,
            bg="#eef2f7"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # -----------------------------------------------------
        # LEFT PANEL
        # -----------------------------------------------------

        left = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid",
            width=390
        )

        left.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        left.pack_propagate(False)

        header = tk.Frame(
            left,
            bg="white"
        )

        header.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            header,
            text="My Notes",
            bg="white",
            fg="#172033",
            font=("Segoe UI", 17, "bold")
        ).pack(
            side="left"
        )

        self.note_count_label = tk.Label(
            header,
            text="",
            bg="white",
            fg="#667085",
            font=("Segoe UI", 9)
        )

        self.note_count_label.pack(
            side="right"
        )

        # Search

        search_frame = tk.Frame(
            left,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            fill="x",
            ipady=6
        )

        self.search_var.trace_add(
            "write",
            self.search_notes
        )

        # Tree

        tree_frame = tk.Frame(
            left,
            bg="white"
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.notes_tree = ttk.Treeview(
            tree_frame,
            columns=(
                "title",
                "date"
            ),
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )

        scrollbar.config(
            command=self.notes_tree.yview
        )

        self.notes_tree.heading(
            "title",
            text="Title"
        )

        self.notes_tree.heading(
            "date",
            text="Updated"
        )

        self.notes_tree.column(
            "title",
            width=220,
            anchor="w"
        )

        self.notes_tree.column(
            "date",
            width=120,
            anchor="center"
        )

        self.notes_tree.pack(
            fill="both",
            expand=True
        )

        self.notes_tree.bind(
            "<<TreeviewSelect>>",
            self.select_note
        )

        # -----------------------------------------------------
        # RIGHT PANEL
        # -----------------------------------------------------

        right = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )

        right.pack(
            side="left",
            fill="both",
            expand=True
        )

        editor_header = tk.Frame(
            right,
            bg="white"
        )

        editor_header.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.editor_title_label = tk.Label(
            editor_header,
            text="Create a New Note",
            bg="white",
            fg="#172033",
            font=("Segoe UI", 17, "bold")
        )

        self.editor_title_label.pack(
            side="left"
        )

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        tk.Label(
            right,
            text="Title",
            bg="white",
            fg="#344054",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=20
        )

        self.title_entry = tk.Entry(
            right,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )

        self.title_entry.pack(
            fill="x",
            padx=20,
            pady=(6, 15),
            ipady=7
        )

        # -----------------------------------------------------
        # CONTENT
        # -----------------------------------------------------

        tk.Label(
            right,
            text="Note",
            bg="white",
            fg="#344054",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=20
        )

        content_frame = tk.Frame(
            right,
            bg="white"
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(6, 10)
        )

        content_scroll = ttk.Scrollbar(
            content_frame,
            orient="vertical"
        )

        content_scroll.pack(
            side="right",
            fill="y"
        )

        self.content_text = tk.Text(
            content_frame,
            wrap="word",
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            undo=True,
            yscrollcommand=content_scroll.set
        )

        content_scroll.config(
            command=self.content_text.yview
        )

        self.content_text.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # DATE
        # -----------------------------------------------------

        self.date_label = tk.Label(
            right,
            text="",
            bg="white",
            fg="#667085",
            font=("Segoe UI", 9)
        )

        self.date_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        # -----------------------------------------------------
        # BUTTON BAR
        # -----------------------------------------------------

        buttons = tk.Frame(
            right,
            bg="white"
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 18)
        )

        tk.Button(
            buttons,
            text="NEW NOTE",
            command=self.new_note,
            bg="#344054",
            fg="white",
            activebackground="#475467",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="left",
            padx=(0, 8),
            ipadx=8,
            ipady=5
        )

        tk.Button(
            buttons,
            text="SAVE NOTE",
            command=self.save_note,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="left",
            padx=(0, 8),
            ipadx=8,
            ipady=5
        )

        tk.Button(
            buttons,
            text="DELETE",
            command=self.delete_note,
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="left",
            padx=(0, 8),
            ipadx=8,
            ipady=5
        )

        tk.Button(
            buttons,
            text="EXPORT ALL",
            command=self.export_notes,
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(
            side="right",
            ipadx=8,
            ipady=5
        )

        self.load_notes()

        self.new_note()

        self.search_entry.focus_set()

    # =========================================================
    # NOTES
    # =========================================================

    def load_notes(self):

        for item in self.notes_tree.get_children():

            self.notes_tree.delete(
                item
            )

        search = self.search_var.get()

        notes = self.database.get_notes(
            self.current_user["id"],
            search
        )

        for note in notes:

            title = note["title"]

            if len(title) > 32:
                title = title[:29] + "..."

            updated = note["updated_at"]

            if len(updated) >= 16:
                updated = updated[:16]

            self.notes_tree.insert(
                "",
                "end",
                iid=str(note["id"]),
                values=(
                    title,
                    updated
                )
            )

        total = len(notes)

        self.note_count_label.config(
            text="{} note{}".format(
                total,
                "" if total == 1 else "s"
            )
        )

    def search_notes(
        self,
        *args
    ):

        if hasattr(
            self,
            "notes_tree"
        ):
            self.load_notes()

    def select_note(
        self,
        event=None
    ):

        selection = self.notes_tree.selection()

        if not selection:
            return

        try:
            note_id = int(
                selection[0]
            )
        except ValueError:
            return

        note = self.database.get_note(
            note_id,
            self.current_user["id"]
        )

        if not note:
            return

        self.current_note_id = note_id

        self.editor_title_label.config(
            text="Edit Note"
        )

        self.title_entry.delete(
            0,
            tk.END
        )

        self.title_entry.insert(
            0,
            note["title"]
        )

        self.content_text.delete(
            "1.0",
            tk.END
        )

        self.content_text.insert(
            "1.0",
            note["content"]
        )

        self.date_label.config(
            text="Created: {}    Updated: {}".format(
                note["created_at"],
                note["updated_at"]
            )
        )

    def new_note(self):

        self.current_note_id = None

        self.editor_title_label.config(
            text="Create a New Note"
        )

        self.title_entry.delete(
            0,
            tk.END
        )

        self.content_text.delete(
            "1.0",
            tk.END
        )

        self.date_label.config(
            text="New note"
        )

        self.title_entry.focus_set()

        try:
            self.notes_tree.selection_remove(
                self.notes_tree.selection()
            )
        except Exception:
            pass

    def save_note(self):

        title = self.title_entry.get().strip()

        content = self.content_text.get(
            "1.0",
            "end-1c"
        ).strip()

        if not title:

            messagebox.showwarning(
                "Save Note",
                "Please enter a note title."
            )

            self.title_entry.focus_set()

            return

        if len(title) > MAX_NOTE_TITLE_LENGTH:

            messagebox.showwarning(
                "Save Note",
                "Title must not exceed {} characters.".format(
                    MAX_NOTE_TITLE_LENGTH
                )
            )

            return

        if not content:

            messagebox.showwarning(
                "Save Note",
                "Please enter some note content."
            )

            self.content_text.focus_set()

            return

        if self.current_note_id is None:

            self.database.create_note(
                self.current_user["id"],
                title,
                content
            )

            messagebox.showinfo(
                "Saved",
                "Note saved successfully."
            )

        else:

            success = self.database.update_note(
                self.current_note_id,
                self.current_user["id"],
                title,
                content
            )

            if not success:

                messagebox.showerror(
                    "Save Note",
                    "The note could not be updated."
                )

                return

            messagebox.showinfo(
                "Saved",
                "Note updated successfully."
            )

        self.load_notes()

        self.select_note_by_title(
            title
        )

    def select_note_by_title(
        self,
        title
    ):

        for item in self.notes_tree.get_children():

            values = self.notes_tree.item(
                item,
                "values"
            )

            if values and values[0] == title:
                self.notes_tree.selection_set(
                    item
                )

                self.notes_tree.focus(
                    item
                )

                self.notes_tree.see(
                    item
                )

                break

    def delete_note(self):

        if self.current_note_id is None:

            messagebox.showwarning(
                "Delete Note",
                "Please select a note first."
            )

            return

        answer = messagebox.askyesno(
            "Delete Note",
            "Are you sure you want to permanently delete this note?"
        )

        if not answer:
            return

        success = self.database.delete_note(
            self.current_note_id,
            self.current_user["id"]
        )

        if not success:

            messagebox.showerror(
                "Delete Note",
                "The note could not be deleted."
            )

            return

        messagebox.showinfo(
            "Delete Note",
            "Note deleted successfully."
        )

        self.load_notes()

        self.new_note()

    # =========================================================
    # EXPORT
    # =========================================================

    def export_notes(self):

        count = self.database.note_count(
            self.current_user["id"]
        )

        if count == 0:

            messagebox.showinfo(
                "Export",
                "You do not have any notes to export."
            )

            return

        path = filedialog.asksaveasfilename(
            title="Export Notes",
            defaultextension=".txt",
            filetypes=[
                (
                    "Text files",
                    "*.txt"
                ),
                (
                    "All files",
                    "*.*"
                )
            ],
            initialfile="my_notes.txt"
        )

        if not path:
            return

        try:

            self.database.export_notes(
                self.current_user["id"],
                path
            )

            messagebox.showinfo(
                "Export",
                "All notes were exported successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Export",
                "Export failed:\n{}".format(
                    error
                )
            )

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Do you want to log out?"
        )

        if not answer:
            return

        self.current_user = None
        self.current_note_id = None

        self.show_login_screen()

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        try:
            self.database.close()
        except Exception:
            pass

        self.root.destroy()
