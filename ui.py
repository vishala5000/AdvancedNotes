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

    # =========================================================
    # COLORS
    # =========================================================

    BG = "#F4F6F8"
    WHITE = "#FFFFFF"

    SIDEBAR = "#172033"
    SIDEBAR_LIGHT = "#202B3D"

    TEXT = "#172033"
    MUTED = "#667085"
    BORDER = "#D0D5DD"

    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"

    SUCCESS = "#16A34A"
    SUCCESS_HOVER = "#15803D"

    DANGER = "#DC2626"
    DANGER_HOVER = "#B91C1C"

    WARNING = "#D97706"

    INPUT_BG = "#FFFFFF"

    # =========================================================
    # CONSTRUCTOR
    # =========================================================

    def __init__(
        self,
        root,
        database
    ):

        self.root = root
        self.database = database

        self.current_user = None
        self.current_note_id = None

        self.original_title = ""
        self.original_content = ""

        self.is_editing = False

        self.search_var = None

        self.title_entry = None
        self.content_text = None
        self.notes_tree = None

        self.status_label = None
        self.date_label = None
        self.character_label = None

        self.setup_window()
        self.setup_styles()

        self.show_login_screen()

    # =========================================================
    # WINDOW
    # =========================================================

    def setup_window(self):

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
            950,
            620
        )

        self.root.configure(
            bg=self.BG
        )

        try:
            self.root.iconname(APP_NAME)
        except Exception:
            pass

    # =========================================================
    # STYLES
    # =========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            background=self.WHITE,
            foreground=self.TEXT,
            fieldbackground=self.WHITE,
            borderwidth=0,
            rowheight=38,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#F2F4F7",
            foreground=self.TEXT,
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#DBEAFE")
            ],
            foreground=[
                ("selected", "#1E3A8A")
            ]
        )

        style.configure(
            "Vertical.TScrollbar",
            troughcolor="#F2F4F7",
            background="#98A2B3",
            borderwidth=0,
            arrowsize=12
        )

    # =========================================================
    # HELPERS
    # =========================================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def create_button(
        self,
        parent,
        text,
        command,
        background,
        foreground="white",
        width=None
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=background,
            activeforeground=foreground,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=8
        )

        if width:
            button.config(
                width=width
            )

        return button

    def create_label(
        self,
        parent,
        text,
        size=10,
        bold=False,
        foreground=None,
        background=None
    ):

        return tk.Label(
            parent,
            text=text,
            bg=background if background else self.WHITE,
            fg=foreground if foreground else self.TEXT,
            font=(
                "Segoe UI",
                size,
                "bold" if bold else "normal"
            )
        )

    # =========================================================
    # LOGIN SCREEN
    # =========================================================

    def show_login_screen(self):

        self.clear_window()

        self.root.title(
            "{} - Login".format(APP_NAME)
        )

        outer = tk.Frame(
            self.root,
            bg=self.BG
        )

        outer.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # CENTER CARD
        # -----------------------------------------------------

        card = tk.Frame(
            outer,
            bg=self.WHITE,
            bd=1,
            relief="solid",
            padx=50,
            pady=40
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Logo/title

        tk.Label(
            card,
            text="NOTES",
            bg=self.PRIMARY,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=8,
            height=2
        ).pack(
            pady=(0, 20)
        )

        tk.Label(
            card,
            text="Welcome Back",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 24, "bold")
        ).pack()

        tk.Label(
            card,
            text="Sign in to access your personal notes",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 10)
        ).pack(
            pady=(5, 30)
        )

        # Username

        tk.Label(
            card,
            text="Username",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.login_username = tk.Entry(
            card,
            width=38,
            font=("Segoe UI", 11),
            bg=self.WHITE,
            fg=self.TEXT,
            relief="solid",
            bd=1
        )

        self.login_username.pack(
            fill="x",
            pady=(6, 18),
            ipady=8
        )

        # Password

        tk.Label(
            card,
            text="Password",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        password_frame = tk.Frame(
            card,
            bg=self.WHITE
        )

        password_frame.pack(
            fill="x",
            pady=(6, 20)
        )

        self.login_password = tk.Entry(
            password_frame,
            font=("Segoe UI", 11),
            bg=self.WHITE,
            fg=self.TEXT,
            show="*",
            relief="solid",
            bd=1
        )

        self.login_password.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        self.login_show_password = tk.BooleanVar(
            value=False
        )

        tk.Checkbutton(
            password_frame,
            text="Show",
            variable=self.login_show_password,
            command=self.toggle_login_password,
            bg=self.WHITE,
            activebackground=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8),
            relief="flat"
        ).pack(
            side="right",
            padx=(8, 0)
        )

        # Login

        self.create_button(
            card,
            "LOGIN",
            self.login,
            self.PRIMARY
        ).pack(
            fill="x",
            pady=(0, 12)
        )

        # Register

        tk.Button(
            card,
            text="Create a new account",
            command=self.show_register_screen,
            bg=self.WHITE,
            fg=self.PRIMARY,
            activebackground=self.WHITE,
            activeforeground=self.PRIMARY_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack()

        tk.Label(
            card,
            text="Your notes are stored locally on this PC.",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(
            pady=(25, 0)
        )

        self.login_username.bind(
            "<Return>",
            lambda event: self.login_password.focus_set()
        )

        self.login_password.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.login_username.focus_set()

    # =========================================================
    # PASSWORD
    # =========================================================

    def toggle_login_password(self):

        if self.login_show_password.get():

            self.login_password.config(
                show=""
            )

        else:

            self.login_password.config(
                show="*"
            )

    def toggle_register_password(self):

        show = ""

        if not self.register_show_password.get():
            show = "*"

        self.register_password.config(
            show=show
        )

        self.register_confirm.config(
            show=show
        )

    # =========================================================
    # REGISTER SCREEN
    # =========================================================

    def show_register_screen(self):

        self.clear_window()

        self.root.title(
            "{} - Create Account".format(APP_NAME)
        )

        outer = tk.Frame(
            self.root,
            bg=self.BG
        )

        outer.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            outer,
            bg=self.WHITE,
            bd=1,
            relief="solid",
            padx=50,
            pady=35
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            card,
            text="Create Account",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 24, "bold")
        ).pack()

        tk.Label(
            card,
            text="Create your secure local notes account",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 10)
        ).pack(
            pady=(5, 25)
        )

        # Username

        tk.Label(
            card,
            text="Username",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.register_username = tk.Entry(
            card,
            width=38,
            font=("Segoe UI", 11),
            bg=self.WHITE,
            fg=self.TEXT,
            relief="solid",
            bd=1
        )

        self.register_username.pack(
            fill="x",
            pady=(6, 15),
            ipady=8
        )

        # Password

        tk.Label(
            card,
            text="Password",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.register_password = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg=self.WHITE,
            fg=self.TEXT,
            show="*",
            relief="solid",
            bd=1
        )

        self.register_password.pack(
            fill="x",
            pady=(6, 15),
            ipady=8
        )

        # Confirm

        tk.Label(
            card,
            text="Confirm Password",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.register_confirm = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg=self.WHITE,
            fg=self.TEXT,
            show="*",
            relief="solid",
            bd=1
        )

        self.register_confirm.pack(
            fill="x",
            pady=(6, 8),
            ipady=8
        )

        self.register_show_password = tk.BooleanVar(
            value=False
        )

        tk.Checkbutton(
            card,
            text="Show password",
            variable=self.register_show_password,
            command=self.toggle_register_password,
            bg=self.WHITE,
            activebackground=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8),
            relief="flat"
        ).pack(
            anchor="w",
            pady=(0, 18)
        )

        # Create

        self.create_button(
            card,
            "CREATE ACCOUNT",
            self.register,
            self.SUCCESS
        ).pack(
            fill="x",
            pady=(0, 8)
        )

        # Back

        tk.Button(
            card,
            text="← Back to Login",
            command=self.show_login_screen,
            bg=self.WHITE,
            fg=self.PRIMARY,
            activebackground=self.WHITE,
            activeforeground=self.PRIMARY_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack()

        self.register_username.focus_set()

    # =========================================================
    # REGISTER
    # =========================================================

    def register(self):

        username = self.register_username.get().strip()
        password = self.register_password.get()
        confirmation = self.register_confirm.get()

        if not username:

            messagebox.showwarning(
                "Create Account",
                "Please enter a username."
            )

            self.register_username.focus_set()
            return

        if len(username) > 50:

            messagebox.showwarning(
                "Create Account",
                "Username cannot exceed 50 characters."
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Create Account",
                "Password must contain at least 6 characters."
            )

            self.register_password.focus_set()
            return

        if password != confirmation:

            messagebox.showerror(
                "Create Account",
                "Passwords do not match."
            )

            self.register_confirm.focus_set()
            return

        success, message = self.database.register_user(
            username,
            password
        )

        if not success:

            messagebox.showerror(
                "Create Account",
                message
            )

            return

        messagebox.showinfo(
            "Account Created",
            "Your account was created successfully."
        )

        self.show_login_screen()

        self.login_username.insert(
            0,
            username
        )

        self.login_password.focus_set()

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):

        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username:

            messagebox.showwarning(
                "Login",
                "Please enter your username."
            )

            self.login_username.focus_set()
            return

        if not password:

            messagebox.showwarning(
                "Login",
                "Please enter your password."
            )

            self.login_password.focus_set()
            return

        user = self.database.login_user(
            username,
            password
        )

        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

            self.login_password.selection_range(
                0,
                tk.END
            )

            self.login_password.focus_set()

            return

        self.current_user = user

        self.show_main_screen()

    # =========================================================
    # MAIN APPLICATION
    # =========================================================

    def show_main_screen(self):

        self.clear_window()

        self.root.title(
            "{} - {}".format(
                APP_NAME,
                self.current_user["username"]
            )
        )

        # =====================================================
        # ROOT
        # =====================================================

        main = tk.Frame(
            self.root,
            bg=self.BG
        )

        main.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar = tk.Frame(
            main,
            bg=self.SIDEBAR,
            width=235
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(
            False
        )

        # Logo

        logo_frame = tk.Frame(
            sidebar,
            bg=self.SIDEBAR
        )

        logo_frame.pack(
            fill="x",
            padx=18,
            pady=(22, 15)
        )

        tk.Label(
            logo_frame,
            text="N",
            bg=self.PRIMARY,
            fg="white",
            font=("Segoe UI", 16, "bold"),
            width=3,
            height=1
        ).pack(
            side="left"
        )

        tk.Label(
            logo_frame,
            text="Advanced Notes",
            bg=self.SIDEBAR,
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(
            side="left",
            padx=10
        )

        # User

        user_frame = tk.Frame(
            sidebar,
            bg=self.SIDEBAR_LIGHT,
            padx=12,
            pady=12
        )

        user_frame.pack(
            fill="x",
            padx=12,
            pady=(0, 20)
        )

        tk.Label(
            user_frame,
            text="SIGNED IN AS",
            bg=self.SIDEBAR_LIGHT,
            fg="#98A2B3",
            font=("Segoe UI", 7, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            user_frame,
            text=self.current_user["username"],
            bg=self.SIDEBAR_LIGHT,
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # Navigation title

        tk.Label(
            sidebar,
            text="NOTES",
            bg=self.SIDEBAR,
            fg="#98A2B3",
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        # New note

        self.create_button(
            sidebar,
            "+  NEW NOTE",
            self.new_note,
            self.PRIMARY
        ).pack(
            fill="x",
            padx=12,
            pady=(0, 8)
        )

        # Refresh

        self.create_button(
            sidebar,
            "↻  REFRESH",
            self.refresh_notes,
            self.SIDEBAR_LIGHT
        ).pack(
            fill="x",
            padx=12,
            pady=2
        )

        # Export

        self.create_button(
            sidebar,
            "↓  EXPORT NOTES",
            self.export_notes,
            self.SIDEBAR_LIGHT
        ).pack(
            fill="x",
            padx=12,
            pady=2
        )

        # Bottom

        bottom = tk.Frame(
            sidebar,
            bg=self.SIDEBAR
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=15
        )

        self.create_button(
            bottom,
            "LOGOUT",
            self.logout,
            self.DANGER
        ).pack(
            fill="x"
        )

        tk.Label(
            bottom,
            text="Version {}".format(APP_VERSION),
            bg=self.SIDEBAR,
            fg="#667085",
            font=("Segoe UI", 8)
        ).pack(
            pady=(10, 0)
        )

        # =====================================================
        # MAIN CONTENT
        # =====================================================

        content = tk.Frame(
            main,
            bg=self.BG
        )

        content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            content,
            bg=self.WHITE,
            height=70,
            bd=1,
            relief="solid"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text="My Notes",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(
            side="left",
            padx=22
        )

        self.header_count = tk.Label(
            header,
            text="",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.header_count.pack(
            side="left"
        )

        # =====================================================
        # WORK AREA
        # =====================================================

        work = tk.Frame(
            content,
            bg=self.BG
        )

        work.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=14
        )

        # =====================================================
        # NOTES LIST
        # =====================================================

        list_panel = tk.Frame(
            work,
            bg=self.WHITE,
            bd=1,
            relief="solid",
            width=370
        )

        list_panel.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )

        list_panel.pack_propagate(
            False
        )

        # Search

        search_frame = tk.Frame(
            list_panel,
            bg=self.WHITE
        )

        search_frame.pack(
            fill="x",
            padx=14,
            pady=14
        )

        tk.Label(
            search_frame,
            text="SEARCH",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w"
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg="#F9FAFB",
            fg=self.TEXT,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            fill="x",
            pady=(5, 0),
            ipady=7
        )

        self.search_var.trace_add(
            "write",
            self.search_notes
        )

        # Tree

        tree_frame = tk.Frame(
            list_panel,
            bg=self.WHITE
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 14)
        )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            style="Vertical.TScrollbar"
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
            selectmode="browse",
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(
            command=self.notes_tree.yview
        )

        self.notes_tree.heading(
            "title",
            text="NOTE"
        )

        self.notes_tree.heading(
            "date",
            text="UPDATED"
        )

        self.notes_tree.column(
            "title",
            width=225,
            minwidth=150,
            anchor="w"
        )

        self.notes_tree.column(
            "date",
            width=105,
            minwidth=90,
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

        self.notes_tree.bind(
            "<Double-1>",
            self.select_note
        )

        # =====================================================
        # EDITOR
        # =====================================================

        editor = tk.Frame(
            work,
            bg=self.WHITE,
            bd=1,
            relief="solid"
        )

        editor.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Editor top

        editor_top = tk.Frame(
            editor,
            bg=self.WHITE
        )

        editor_top.pack(
            fill="x",
            padx=20,
            pady=(17, 10)
        )

        self.editor_heading = tk.Label(
            editor_top,
            text="New Note",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 17, "bold")
        )

        self.editor_heading.pack(
            side="left"
        )

        self.unsaved_label = tk.Label(
            editor_top,
            text="",
            bg=self.WHITE,
            fg=self.WARNING,
            font=("Segoe UI", 9, "bold")
        )

        self.unsaved_label.pack(
            side="right"
        )

        # Title

        tk.Label(
            editor,
            text="TITLE",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=20
        )

        self.title_entry = tk.Entry(
            editor,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 14, "bold"),
            relief="solid",
            bd=1
        )

        self.title_entry.pack(
            fill="x",
            padx=20,
            pady=(5, 15),
            ipady=8
        )

        # Content

        content_label_frame = tk.Frame(
            editor,
            bg=self.WHITE
        )

        content_label_frame.pack(
            fill="x",
            padx=20
        )

        tk.Label(
            content_label_frame,
            text="CONTENT",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="left"
        )

        self.character_label = tk.Label(
            content_label_frame,
            text="0 characters",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        )

        self.character_label.pack(
            side="right"
        )

        text_frame = tk.Frame(
            editor,
            bg=self.WHITE
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 10)
        )

        text_scroll = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            style="Vertical.TScrollbar"
        )

        text_scroll.pack(
            side="right",
            fill="y"
        )

        self.content_text = tk.Text(
            text_frame,
            wrap="word",
            undo=True,
            font=("Segoe UI", 11),
            bg="#FCFCFD",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="solid",
            bd=1,
            padx=12,
            pady=12,
            yscrollcommand=text_scroll.set
        )

        text_scroll.config(
            command=self.content_text.yview
        )

        self.content_text.pack(
            fill="both",
            expand=True
        )

        self.title_entry.bind(
            "<KeyRelease>",
            self.editor_changed
        )

        self.content_text.bind(
            "<KeyRelease>",
            self.editor_changed
        )

        # Date

        self.date_label = tk.Label(
            editor,
            text="New note",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        )

        self.date_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # =====================================================
        # BUTTON BAR
        # =====================================================

        button_bar = tk.Frame(
            editor,
            bg="#F9FAFB",
            bd=1,
            relief="solid"
        )

        button_bar.pack(
            fill="x"
        )

        button_left = tk.Frame(
            button_bar,
            bg="#F9FAFB"
        )

        button_left.pack(
            side="left",
            padx=14,
            pady=12
        )

        self.new_button = self.create_button(
            button_left,
            "＋ NEW",
            self.new_note,
            self.SIDEBAR_LIGHT
        )

        self.new_button.pack(
            side="left",
            padx=(0, 7)
        )

        self.save_button = self.create_button(
            button_left,
            "✓ SAVE",
            self.save_note,
            self.PRIMARY
        )

        self.save_button.pack(
            side="left",
            padx=(0, 7)
        )

        self.cancel_button = self.create_button(
            button_left,
            "↶ CANCEL",
            self.cancel_editing,
            "#667085"
        )

        self.cancel_button.pack(
            side="left"
        )

        button_right = tk.Frame(
            button_bar,
            bg="#F9FAFB"
        )

        button_right.pack(
            side="right",
            padx=14,
            pady=12
        )

        self.delete_button = self.create_button(
            button_right,
            "DELETE",
            self.delete_note,
            self.DANGER
        )

        self.delete_button.pack(
            side="right"
        )

        # =====================================================
        # STATUS
        # =====================================================

        status = tk.Frame(
            content,
            bg=self.BG,
            height=28
        )

        status.pack(
            fill="x"
        )

        status.pack_propagate(
            False
        )

        self.status_label = tk.Label(
            status,
            text="Ready",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        )

        self.status_label.pack(
            side="left",
            padx=18
        )

        # Keyboard shortcuts

        self.root.bind(
            "<Control-n>",
            lambda event: self.new_note()
        )

        self.root.bind(
            "<Control-s>",
            lambda event: self.save_note()
        )

        self.root.bind(
            "<Control-f>",
            lambda event: self.focus_search()
        )

        self.root.bind(
            "<Escape>",
            lambda event: self.cancel_editing()
        )

        self.load_notes()

        self.new_note()

        self.search_entry.focus_set()

    # =========================================================
    # LOAD NOTES
    # =========================================================

    def load_notes(self):

        if self.notes_tree is None:
            return

        for item in self.notes_tree.get_children():

            self.notes_tree.delete(
                item
            )

        search = ""

        if self.search_var is not None:
            search = self.search_var.get()

        notes = self.database.get_notes(
            self.current_user["id"],
            search
        )

        for note in notes:

            title = note["title"]

            display_title = title

            if len(display_title) > 34:
                display_title = (
                    display_title[:31] +
                    "..."
                )

            date_value = note["updated_at"]

            if len(date_value) >= 16:
                date_value = date_value[:16]

            self.notes_tree.insert(
                "",
                "end",
                iid=str(note["id"]),
                values=(
                    display_title,
                    date_value
                )
            )

        count = self.database.note_count(
            self.current_user["id"]
        )

        if hasattr(
            self,
            "header_count"
        ):

            self.header_count.config(
                text="{} total note{}".format(
                    count,
                    "" if count == 1 else "s"
                )
            )

        self.update_status(
            "{} note{} available".format(
                count,
                "" if count == 1 else "s"
            )
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def search_notes(
        self,
        *args
    ):

        if self.notes_tree is None:
            return

        self.load_notes()

    def focus_search(self):

        if self.search_entry:

            self.search_entry.focus_set()

            self.search_entry.selection_range(
                0,
                tk.END
            )

    # =========================================================
    # SELECT NOTE
    # =========================================================

    def select_note(
        self,
        event=None
    ):

        if self.has_unsaved_changes():

            answer = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes.\n\n"
                "Save them before opening another note?"
            )

            if answer is None:
                return

            if answer:

                if not self.save_note(
                    show_message=False
                ):
                    return

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

        self.load_note_into_editor(
            note
        )

    # =========================================================
    # LOAD NOTE INTO EDITOR
    # =========================================================

    def load_note_into_editor(
        self,
        note
    ):

        self.current_note_id = note["id"]

        self.is_editing = True

        self.original_title = note["title"]
        self.original_content = note["content"]

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

        self.editor_heading.config(
            text="Edit Note"
        )

        self.date_label.config(
            text="Created: {}    •    Updated: {}".format(
                note["created_at"],
                note["updated_at"]
            )
        )

        self.unsaved_label.config(
            text=""
        )

        self.update_character_count()

        self.update_status(
            "Opened note: {}".format(
                note["title"]
            )
        )

        self.title_entry.focus_set()

    # =========================================================
    # NEW NOTE
    # =========================================================

    def new_note(self):

        if self.title_entry is not None:

            if self.has_unsaved_changes():

                answer = messagebox.askyesnocancel(
                    "Unsaved Changes",
                    "You have unsaved changes.\n\n"
                    "Save them before creating a new note?"
                )

                if answer is None:
                    return

                if answer:

                    if not self.save_note(
                        show_message=False
                    ):
                        return

        self.current_note_id = None

        self.is_editing = False

        self.original_title = ""
        self.original_content = ""

        self.title_entry.delete(
            0,
            tk.END
        )

        self.content_text.delete(
            "1.0",
            tk.END
        )

        self.editor_heading.config(
            text="New Note"
        )

        self.date_label.config(
            text="New note — not saved yet"
        )

        self.unsaved_label.config(
            text=""
        )

        self.update_character_count()

        if self.notes_tree:

            try:

                self.notes_tree.selection_remove(
                    self.notes_tree.selection()
                )

            except Exception:
                pass

        self.update_status(
            "Ready to create a new note"
        )

        self.title_entry.focus_set()

    # =========================================================
    # EDITOR CHANGES
    # =========================================================

    def editor_changed(
        self,
        event=None
    ):

        self.update_character_count()

        if self.has_unsaved_changes():

            self.unsaved_label.config(
                text="● Unsaved changes"
            )

            self.update_status(
                "You have unsaved changes"
            )

        else:

            self.unsaved_label.config(
                text=""
            )

    def has_unsaved_changes(self):

        if self.title_entry is None:
            return False

        current_title = self.title_entry.get()

        current_content = self.content_text.get(
            "1.0",
            "end-1c"
        )

        if self.current_note_id is None:

            return bool(
                current_title.strip()
                or current_content.strip()
            )

        return (
            current_title != self.original_title
            or
            current_content != self.original_content
        )

    # =========================================================
    # CHARACTER COUNT
    # =========================================================

    def update_character_count(self):

        if self.content_text is None:
            return

        content = self.content_text.get(
            "1.0",
            "end-1c"
        )

        count = len(content)

        self.character_label.config(
            text="{} character{}".format(
                count,
                "" if count == 1 else "s"
            )
        )

    # =========================================================
    # SAVE NOTE
    # =========================================================

    def save_note(
        self,
        show_message=True
    ):

        title = self.title_entry.get().strip()

        content = self.content_text.get(
            "1.0",
            "end-1c"
        ).strip()

        if not title:

            if show_message:

                messagebox.showwarning(
                    "Save Note",
                    "Please enter a title."
                )

            self.title_entry.focus_set()

            return False

        if len(title) > MAX_NOTE_TITLE_LENGTH:

            if show_message:

                messagebox.showwarning(
                    "Save Note",
                    "The title cannot exceed {} characters.".format(
                        MAX_NOTE_TITLE_LENGTH
                    )
                )

            return False

        if not content:

            if show_message:

                messagebox.showwarning(
                    "Save Note",
                    "Please enter some note content."
                )

            self.content_text.focus_set()

            return False

        # -----------------------------------------------------
        # CREATE
        # -----------------------------------------------------

        if self.current_note_id is None:

            note_id = self.database.create_note(
                self.current_user["id"],
                title,
                content
            )

            self.current_note_id = note_id

            self.is_editing = True

            message = "Note saved successfully."

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        else:

            success = self.database.update_note(
                self.current_note_id,
                self.current_user["id"],
                title,
                content
            )

            if not success:

                if show_message:

                    messagebox.showerror(
                        "Save Note",
                        "The note could not be updated."
                    )

                return False

            message = "Note updated successfully."

        # -----------------------------------------------------
        # UPDATE ORIGINAL VALUES
        # -----------------------------------------------------

        self.original_title = title
        self.original_content = content

        self.unsaved_label.config(
            text=""
        )

        self.load_notes()

        self.select_note_after_save()

        self.update_status(
            message
        )

        if show_message:

            messagebox.showinfo(
                "Saved",
                message
            )

        return True

    # =========================================================
    # SELECT AFTER SAVE
    # =========================================================

    def select_note_after_save(self):

        if not self.current_note_id:
            return

        note = self.database.get_note(
            self.current_note_id,
            self.current_user["id"]
        )

        if not note:
            return

        self.load_note_into_editor(
            note
        )

        try:

            self.notes_tree.selection_set(
                str(self.current_note_id)
            )

            self.notes_tree.focus(
                str(self.current_note_id)
            )

            self.notes_tree.see(
                str(self.current_note_id)
            )

        except Exception:
            pass

    # =========================================================
    # CANCEL
    # =========================================================

    def cancel_editing(self):

        if not self.has_unsaved_changes():

            if self.current_note_id:

                note = self.database.get_note(
                    self.current_note_id,
                    self.current_user["id"]
                )

                if note:

                    self.load_note_into_editor(
                        note
                    )

            else:

                self.new_note()

            return

        answer = messagebox.askyesno(
            "Cancel Changes",
            "Discard all unsaved changes?"
        )

        if not answer:
            return

        if self.current_note_id:

            note = self.database.get_note(
                self.current_note_id,
                self.current_user["id"]
            )

            if note:

                self.load_note_into_editor(
                    note
                )

                self.update_status(
                    "Changes discarded"
                )

        else:

            self.title_entry.delete(
                0,
                tk.END
            )

            self.content_text.delete(
                "1.0",
                tk.END
            )

            self.update_character_count()

            self.unsaved_label.config(
                text=""
            )

            self.update_status(
                "New note cleared"
            )

    # =========================================================
    # DELETE
    # =========================================================

    def delete_note(self):

        if self.current_note_id is None:

            messagebox.showwarning(
                "Delete Note",
                "Select a saved note before deleting."
            )

            return

        note = self.database.get_note(
            self.current_note_id,
            self.current_user["id"]
        )

        if not note:

            messagebox.showerror(
                "Delete Note",
                "The selected note could not be found."
            )

            self.load_notes()
            self.new_note()

            return

        answer = messagebox.askyesno(
            "Delete Note",
            "Delete this note permanently?\n\n"
            "\"{}\"\n\n"
            "This action cannot be undone.".format(
                note["title"]
            ),
            icon="warning"
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

        self.current_note_id = None

        self.load_notes()

        self.new_note()

        self.update_status(
            "Note deleted successfully"
        )

        messagebox.showinfo(
            "Deleted",
            "The note was permanently deleted."
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_notes(self):

        if self.has_unsaved_changes():

            answer = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes.\n\n"
                "Save them before refreshing?"
            )

            if answer is None:
                return

            if answer:

                if not self.save_note(
                    show_message=False
                ):
                    return

        self.load_notes()

        self.update_status(
            "Notes refreshed"
        )

    # =========================================================
    # EXPORT
    # =========================================================

    def export_notes(self):

        count = self.database.note_count(
            self.current_user["id"]
        )

        if count == 0:

            messagebox.showinfo(
                "Export Notes",
                "There are no notes to export."
            )

            return

        path = filedialog.asksaveasfilename(
            title="Export All Notes",
            defaultextension=".txt",
            filetypes=[
                (
                    "Text Files",
                    "*.txt"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ],
            initialfile="My-Notes.txt"
        )

        if not path:
            return

        try:

            self.database.export_notes(
                self.current_user["id"],
                path
            )

            self.update_status(
                "All notes exported successfully"
            )

            messagebox.showinfo(
                "Export Complete",
                "All {} note{} exported successfully.".format(
                    count,
                    "" if count == 1 else "s"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Export Failed",
                "Could not export notes.\n\n{}".format(
                    error
                )
            )

    # =========================================================
    # STATUS
    # =========================================================

    def update_status(
        self,
        text
    ):

        if self.status_label:

            self.status_label.config(
                text=text
            )

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        if self.has_unsaved_changes():

            answer = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes.\n\n"
                "Save them before logging out?"
            )

            if answer is None:
                return

            if answer:

                if not self.save_note(
                    show_message=False
                ):
                    return

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to log out?"
        )

        if not answer:
            return

        self.current_user = None
        self.current_note_id = None

        self.show_login_screen()

    # =========================================================
    # CLOSE APPLICATION
    # =========================================================

    def close(self):

        if self.has_unsaved_changes():

            answer = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes.\n\n"
                "Save before closing?"
            )

            if answer is None:
                return

            if answer:

                if not self.save_note(
                    show_message=False
                ):
                    return

        try:

            self.database.close()

        except Exception:
            pass

        self.root.destroy()
