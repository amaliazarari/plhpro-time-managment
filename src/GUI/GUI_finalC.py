import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os, pickle

#Τα παρακάτω σχόλια είναι ο αρχικός κώδικας του αρχείου GUI από την Αμαλία Ζαράρη
# import tkinter as tk
# import tkinter
# from tkinter import ttk
# from tkinter import *
#
# #κουμπιά
# def logIn():
#     output.delete("1.0",tk.END) #καθαρίζει το frame
#     output.insert(tk.END, f"a. Για εισαγωγή νέων χρηστών: \nb. Σύνδεση χρήστη:\n")
#     return
#
# def b2pushed():
#     output.delete("1.0", tk.END) #καθαρίζει το frame
#     output.insert(tk.END,"KANE KATI\n\n")
#     return
#
# def b3pushed():
#     output.delete("1.0", tk.END) #καθαρίζει το frame
#     output.insert(tk.END,"KANE KATI\n")
#     return
#
# def b5pushed():
#     window.destroy()#τερματισμός παραθύρου
#     return
#
# window = tk.Tk() #φτιάχνω παράθυρο
# window.title("Project53 (Διαχείριση Χρόνου)") #τίτλος παραθύρου πάνω αριστερά
# window.minsize(width=350, height=600) #ελάχιστο μέγεθος παραθύρου
#
# left = tk.Frame(window)
# left.pack(side = "left")
#
# right = tk.Frame(window)
# right.pack(side= "right")
#
# tkinter.Label(window, text="Εφαρμογή Διαχείρισης Χρόνου Υποχρεώσεων & Ελεύθερου Χρόνου").pack()
# tkinter.Label(window, text="\n=== MENOY ΔΙΑΧΕΙΡΙΣΗΣ ΧΡΟΝΟΥ ===").pack()
#
# #Απλά κουμπιά print
# btnTotal = tkinter.Button(left,text="Εισαγωγή Δεδομένων",command=logIn, width=40)
# btnTotal.pack()
# btnMaxMin = tkinter.Button(left,text="Push a)",command=b2pushed, width=40)
# btnMaxMin.pack()
# movingAvgBtn = tkinter.Button(left,text="Push b)",command=b3pushed, width=40)
# movingAvgBtn.pack()
# exitBtn = tkinter.Button(left,text="2. Έξοδος", bg='salmon', fg="white smoke",command=b5pushed, width=40)
# exitBtn.pack()
#
# output = tkinter.Text(right , width=60)
# output.pack()
#
# window.mainloop()

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usersDB.dat")


class TimeManagementGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Project 53 - Εφαρμογή Διαχείρισης Χρόνου")
        self.root.geometry("1100x680")
        self.root.minsize(900, 560)

        self.users = []
        self.current_user = None

        self.load_users()

        # Αν δεν υπάρχουν χρήστες, δημιουργία πρώτου Admin
        if not self.users:
            self._create_first_admin()
        else:
            self._build_ui()
            self.write_result("Καλώς ήρθατε!\n\nΠατήστε «Σύνδεση / Εγγραφή» για να ξεκινήσετε.")

    # ── ΔΕΔΟΜΕΝΑ ──────────────────────────────────────────────────────────────

    def load_users(self):
        if not os.path.exists(DB):
            self.users = []
            return
        try:
            with open(DB, "rb") as f:
                self.users = pickle.load(f)
        except Exception:
            self.users = []

    def save_users(self):
        with open(DB, "wb") as f:
            pickle.dump(self.users, f)

    def find_user(self, email):
        return next((u for u in self.users if u["email"] == email), None)

    def authenticate_user(self, email, pw):
        return next((u for u in self.users
                     if u["email"] == email and u["password"] == pw), None)

    def admin_exists(self):
        return any(u.get("role") == "admin" for u in self.users)

    @staticmethod
    def optimal_schedule(user):
        sorted_acts = sorted(user["activities"], key=lambda a: a["priority"], reverse=True)
        feasible, infeasible, rem = [], [], user["hours"]
        for a in sorted_acts:
            if a["time"] <= rem:
                feasible.append(a)
                rem -= a["time"]
            else:
                infeasible.append(a)
        return feasible, infeasible, rem

    # ── ΔΗΜΙΟΥΡΓΙΑ ΠΡΩΤΟΥ ADMIN ───────────────────────────────────────────────

    def _create_first_admin(self):
        """Αν δεν υπάρχουν χρήστες, εμφανίζει φόρμα δημιουργίας πρώτου Admin."""
        win = tk.Toplevel(self.root)
        win.title("Δημιουργία Πρώτου Admin")
        win.resizable(False, False)
        win.grab_set()
        win.geometry("380x280")
        win.update_idletasks()
        win.geometry(f"+{self.root.winfo_screenwidth()//2 - 190}+{self.root.winfo_screenheight()//2 - 140}")

        tk.Label(win, text="Δεν υπάρχουν χρήστες στο σύστημα.",
                 font=("Arial", 10)).pack(pady=(16, 4))
        tk.Label(win, text="Δημιουργία πρώτου Admin:",
                 font=("Arial", 10, "bold")).pack(pady=(0, 10))

        form = tk.Frame(win, padx=20)
        form.pack(fill="x")

        fields = [("Όνομα:", False), ("Email:", False),
                  ("Κωδικός:", True), ("Ώρες/εβδ.:", False)]
        entries = []
        for i, (lbl, secret) in enumerate(fields):
            tk.Label(form, text=lbl).grid(row=i, column=0, sticky="w", pady=4)
            e = tk.Entry(form, width=28, show="*" if secret else "")
            e.grid(row=i, column=1, pady=4)
            entries.append(e)

        def do_create():
            name, email, pw, h_str = [e.get().strip() for e in entries]
            if not all([name, email, pw, h_str]):
                messagebox.showwarning("Προσοχή", "Συμπληρώστε όλα τα πεδία.", parent=win)
                return
            try:
                h = float(h_str)
                assert h > 0
            except Exception:
                messagebox.showerror("Σφάλμα", "Εισάγετε έγκυρο θετικό αριθμό ωρών.", parent=win)
                return
            new_u = {"name": name, "email": email, "password": pw,
                     "hours": h, "activities": [], "role": "admin"}
            self.users.append(new_u)
            self.save_users()
            win.destroy()
            self._build_ui()
            self.write_result(f"Ο πρώτος Admin «{name}» δημιουργήθηκε!\n\nΠατήστε «Σύνδεση» για να συνδεθείτε.")

        tk.Button(win, text="Δημιουργία Admin", command=do_create,
                  width=22).pack(pady=14)

        # Κλείσιμο εφαρμογής αν κλείσει το παράθυρο χωρίς δημιουργία
        win.protocol("WM_DELETE_WINDOW", self.root.destroy)

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = self.root

        tk.Label(root,
                 text="Εφαρμογή Διαχείρισης Χρόνου Υποχρεώσεων & Ελεύθερου Χρόνου",
                 font=("Arial", 14, "bold")).pack(pady=(10, 2))

        self.lbl_user = tk.Label(root, text="Μη συνδεδεμένος",
                                 font=("Arial", 9), fg="gray")
        self.lbl_user.pack()

        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=6)

        # ── ΑΡΙΣΤΕΡΑ ──
        left = tk.Frame(main_frame)
        left.pack(side="left", fill="y", padx=(0, 8))

        # Λογαριασμός
        frm_account = tk.LabelFrame(left, text="Λογαριασμός", padx=8, pady=6)
        frm_account.pack(fill="x", pady=(0, 6))

        self.btn_login = tk.Button(frm_account, text="Σύνδεση",
                                   command=self.open_login_window, width=26)
        self.btn_login.pack(pady=2)

        self.btn_logout = tk.Button(frm_account, text="Αποσύνδεση",
                                    command=self.do_logout, width=26, state="disabled")
        self.btn_logout.pack(pady=2)

        # Καταχώριση
        frm_form = tk.LabelFrame(left, text="Καταχώριση Δραστηριότητας", padx=8, pady=6)
        frm_form.pack(fill="x", pady=(0, 6))

        tk.Label(frm_form, text="Όνομα δραστηριότητας:").pack(anchor="w")
        self.entry_name = tk.Entry(frm_form, width=30)
        self.entry_name.pack(pady=(0, 4))

        tk.Label(frm_form, text="Ώρες ανά εβδομάδα:").pack(anchor="w")
        self.entry_hours = tk.Entry(frm_form, width=30)
        self.entry_hours.pack(pady=(0, 4))

        tk.Label(frm_form, text="Σημαντικότητα (1-10):").pack(anchor="w")
        self.spin_priority = tk.Spinbox(frm_form, from_=1, to=10, width=28)
        self.spin_priority.pack(pady=(0, 4))

        tk.Label(frm_form, text="Κατηγορία:").pack(anchor="w")
        self.combo_category = ttk.Combobox(frm_form,
                                           values=["Υποχρέωση", "Ελεύθερος Χρόνος"],
                                           state="readonly", width=27)
        self.combo_category.current(0)
        self.combo_category.pack(pady=(0, 4))

        self.btn_add = tk.Button(frm_form, text="Προσθήκη δραστηριότητας",
                                 command=self.add_activity, width=28, state="disabled")
        self.btn_add.pack(pady=(4, 2))

        self.btn_edit = tk.Button(frm_form, text="Επεξεργασία επιλεγμένης",
                                  command=self.edit_activity, width=28, state="disabled")
        self.btn_edit.pack(pady=2)

        self.btn_del = tk.Button(frm_form, text="Διαγραφή επιλεγμένης",
                                 command=self.delete_activity, width=28, state="disabled")
        self.btn_del.pack(pady=2)

        # Ενέργειες
        frm_actions = tk.LabelFrame(left, text="Ενέργειες", padx=8, pady=6)
        frm_actions.pack(fill="x", pady=(0, 6))

        self.btn_stats = tk.Button(frm_actions, text="Στατιστικά",
                                   command=self.show_statistics, width=28, state="disabled")
        self.btn_stats.pack(pady=2)

        self.btn_optimal = tk.Button(frm_actions, text="Βέλτιστη Διαχείριση",
                                     command=self.show_optimal, width=28, state="disabled")
        self.btn_optimal.pack(pady=2)

        self.btn_chart = tk.Button(frm_actions, text="Γράφημα",
                                   command=self.show_chart, width=28, state="disabled")
        self.btn_chart.pack(pady=2)

        # Admin Panel (ορατό μόνο σε admin)
        self.frm_admin = tk.LabelFrame(left, text="⚙ Admin Panel", padx=8, pady=6)
        # Δεν κάνουμε pack ακόμα — θα γίνει μόνο αν ο χρήστης είναι admin

        self.btn_admin_users = tk.Button(self.frm_admin, text="Διαχείριση Χρηστών",
                                         command=self.open_admin_users, width=28)
        self.btn_admin_users.pack(pady=2)

        # Αρχεία
        frm_files = tk.LabelFrame(left, text="Αρχεία", padx=8, pady=6)
        frm_files.pack(fill="x", pady=(0, 6))

        self.btn_save_dat = tk.Button(frm_files, text="Αποθήκευση δεδομένων (.dat)",
                                      command=self.save_data, width=28, state="disabled")
        self.btn_save_dat.pack(pady=2)

        self.btn_load_dat = tk.Button(frm_files, text="Φόρτωση δεδομένων (.dat)",
                                      command=self.load_data, width=28, state="disabled")
        self.btn_load_dat.pack(pady=2)

        self.btn_exp_dat = tk.Button(frm_files, text="Εξαγωγή δεδομένων (.dat)",
                                     command=self.export_dat, width=28, state="disabled")
        self.btn_exp_dat.pack(pady=2)

        self.btn_imp_dat = tk.Button(frm_files, text="Εισαγωγή δεδομένων (.dat)",
                                     command=self.import_dat, width=28, state="disabled")
        self.btn_imp_dat.pack(pady=2)

        tk.Button(left, text="Έξοδος", command=root.destroy,
                  bg="salmon", fg="white smoke", width=28).pack(pady=4)

        self.buttons_need_login = [
            self.btn_add, self.btn_edit, self.btn_del,
            self.btn_stats, self.btn_optimal, self.btn_chart,
            self.btn_save_dat, self.btn_load_dat,
            self.btn_exp_dat, self.btn_imp_dat,
        ]

        # ── ΔΕΞΙΑ ──
        right = tk.Frame(main_frame)
        right.pack(side="left", fill="both", expand=True)

        frm_table = tk.LabelFrame(right, text="Δραστηριότητες", padx=6, pady=4)
        frm_table.pack(fill="both", expand=True)

        cols = ("Δραστηριότητα", "Κατηγορία", "Ώρες/εβδ.", "Σημαντ.")
        self.tree = ttk.Treeview(frm_table, columns=cols, show="headings", height=16)
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.column("Δραστηριότητα", width=220, anchor="w")
        self.tree.column("Κατηγορία",     width=160, anchor="center")
        self.tree.column("Ώρες/εβδ.",     width=90,  anchor="center")
        self.tree.column("Σημαντ.",        width=80,  anchor="center")

        sb_tree = ttk.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb_tree.set)
        sb_tree.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        frm_result = tk.LabelFrame(right, text="Αποτελέσματα", padx=6, pady=4)
        frm_result.pack(fill="x")

        self.result_text = tk.Text(frm_result, height=9, font=("Courier", 9),
                                   state="disabled", wrap="word",
                                   relief="sunken", bd=1)
        sb_res = ttk.Scrollbar(frm_result, orient="vertical",
                               command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=sb_res.set)
        sb_res.pack(side="right", fill="y")
        self.result_text.pack(fill="x")

    # ── ΒΟΗΘΗΤΙΚΕΣ ────────────────────────────────────────────────────────────

    def write_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_hours.delete(0, tk.END)
        self.spin_priority.delete(0, tk.END)
        self.spin_priority.insert(0, "5")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        if not self.current_user:
            return
        for act in self.current_user["activities"]:
            self.tree.insert("", "end", values=(
                act["name"], act["category"],
                f"{act['time']}h", f"{act['priority']}/10"))

    def set_buttons_state(self, logged_in):
        state = "normal" if logged_in else "disabled"
        for b in self.buttons_need_login:
            b.config(state=state)
        self.btn_login.config(state="disabled" if logged_in else "normal")
        self.btn_logout.config(state=state)

        # Admin panel: εμφανίζεται μόνο αν ο συνδεδεμένος είναι admin
        if logged_in and self.current_user.get("role") == "admin":
            self.frm_admin.pack(fill="x", pady=(0, 6),
                                before=self.btn_save_dat.master)
        else:
            self.frm_admin.pack_forget()

        role_label = " [Admin]" if (logged_in and self.current_user.get("role") == "admin") else ""
        self.lbl_user.config(
            text=f"Συνδεδεμένος: {self.current_user['name']}{role_label}" if logged_in
            else "Μη συνδεδεμένος"
        )

    def validate_hours(self, val_str, parent=None):
        try:
            v = float(val_str)
            assert v > 0
            return v
        except Exception:
            messagebox.showerror("Σφάλμα", "Εισάγετε έγκυρο θετικό αριθμό ωρών.",
                                 parent=parent)
            return None

    # ── ΣΥΝΔΕΣΗ ───────────────────────────────────────────────────────────────

    def open_login_window(self):
        win = tk.Toplevel(self.root)
        win.title("Σύνδεση")
        win.resizable(False, False)
        win.grab_set()
        win.geometry("340x200")
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width()  - 340) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        win.geometry(f"+{x}+{y}")

        tk.Label(win, text="Σύνδεση", font=("Arial", 11, "bold")).pack(pady=12)

        form = tk.Frame(win, padx=20)
        form.pack(fill="x")

        tk.Label(form, text="Email:").grid(row=0, column=0, sticky="w", pady=6)
        e_email = tk.Entry(form, width=28)
        e_email.grid(row=0, column=1, pady=6)

        tk.Label(form, text="Κωδικός:").grid(row=1, column=0, sticky="w", pady=6)
        e_pass = tk.Entry(form, width=28, show="*")
        e_pass.grid(row=1, column=1, pady=6)

        def do_login():
            u = self.authenticate_user(e_email.get().strip(), e_pass.get())
            if u:
                self.current_user = u
                win.destroy()
                self.set_buttons_state(True)
                self.refresh_tree()
                role_str = "Admin" if u.get("role") == "admin" else "Χρήστης"
                self.write_result(
                    f"Καλώς ήρθατε, {u['name']}! ({role_str})\n"
                    f"Διαθέσιμες ώρες: {u['hours']}h/εβδ.\n"
                    f"Δραστηριότητες : {len(u['activities'])}")
            else:
                messagebox.showerror("Σφάλμα", "Λανθασμένο email ή κωδικός.", parent=win)

        e_pass.bind("<Return>", lambda e: do_login())
        tk.Button(win, text="Σύνδεση", command=do_login, width=20).pack(pady=12)

    def do_logout(self):
        if messagebox.askyesno("Αποσύνδεση", "Αποθήκευση & αποσύνδεση;"):
            self.save_users()
        self.current_user = None
        self.set_buttons_state(False)
        self.tree.delete(*self.tree.get_children())
        self.write_result("Αποσυνδεθήκατε.")

    # ── ADMIN: ΔΙΑΧΕΙΡΙΣΗ ΧΡΗΣΤΩΝ ─────────────────────────────────────────────

    def open_admin_users(self):
        """Παράθυρο Admin για διαχείριση χρηστών (προσθήκη / διαγραφή)."""
        win = tk.Toplevel(self.root)
        win.title("Admin — Διαχείριση Χρηστών")
        win.grab_set()
        win.geometry("600x440")
        x = self.root.winfo_x() + (self.root.winfo_width()  - 600) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 440) // 2
        win.geometry(f"+{x}+{y}")

        tk.Label(win, text="Διαχείριση Χρηστών",
                 font=("Arial", 11, "bold")).pack(pady=8)

        # Πίνακας χρηστών
        frm_tbl = tk.Frame(win)
        frm_tbl.pack(fill="both", expand=True, padx=10)

        cols = ("Όνομα", "Email", "Ρόλος", "Ώρες/εβδ.")
        utree = ttk.Treeview(frm_tbl, columns=cols, show="headings", height=10)
        for col in cols:
            utree.heading(col, text=col)
        utree.column("Όνομα",    width=140, anchor="w")
        utree.column("Email",    width=190, anchor="w")
        utree.column("Ρόλος",   width=80,  anchor="center")
        utree.column("Ώρες/εβδ.", width=90, anchor="center")

        sb = ttk.Scrollbar(frm_tbl, orient="vertical", command=utree.yview)
        utree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        utree.pack(fill="both", expand=True)

        def refresh_utree():
            utree.delete(*utree.get_children())
            for u in self.users:
                utree.insert("", "end", values=(
                    u["name"], u["email"],
                    u.get("role", "user"), f"{u['hours']}h"))

        refresh_utree()

        # Κουμπιά
        frm_btns = tk.Frame(win)
        frm_btns.pack(pady=8)

        def del_user():
            sel = utree.selection()
            if not sel:
                messagebox.showinfo("Πληροφορία", "Επιλέξτε χρήστη.", parent=win)
                return
            idx = utree.index(sel[0])
            u = self.users[idx]
            if u["email"] == self.current_user["email"]:
                messagebox.showerror("Σφάλμα", "Δεν μπορείτε να διαγράψετε τον εαυτό σας.", parent=win)
                return
            if messagebox.askyesno("Διαγραφή", f"Να διαγραφεί ο χρήστης «{u['name']}»;", parent=win):
                self.users.pop(idx)
                self.save_users()
                refresh_utree()

        tk.Button(frm_btns, text="Προσθήκη Χρήστη",
                  command=lambda: self._add_user_dialog(win, refresh_utree),
                  width=20).pack(side="left", padx=6)
        tk.Button(frm_btns, text="Διαγραφή Επιλεγμένου",
                  command=del_user, width=20).pack(side="left", padx=6)
        tk.Button(frm_btns, text="Κλείσιμο",
                  command=win.destroy, width=14).pack(side="left", padx=6)

    def _add_user_dialog(self, parent, on_success):
        """Διάλογος προσθήκης νέου χρήστη από Admin."""
        win = tk.Toplevel(parent)
        win.title("Προσθήκη Χρήστη")
        win.resizable(False, False)
        win.grab_set()
        win.geometry("360x280")
        x = parent.winfo_x() + (parent.winfo_width()  - 360) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 280) // 2
        win.geometry(f"+{x}+{y}")

        tk.Label(win, text="Νέος Χρήστης",
                 font=("Arial", 10, "bold")).pack(pady=10)

        form = tk.Frame(win, padx=16)
        form.pack(fill="x")

        fields = [("Όνομα:", False), ("Email:", False),
                  ("Κωδικός:", True), ("Ώρες/εβδ.:", False)]
        entries = []
        for i, (lbl, secret) in enumerate(fields):
            tk.Label(form, text=lbl).grid(row=i, column=0, sticky="w", pady=4)
            e = tk.Entry(form, width=26, show="*" if secret else "")
            e.grid(row=i, column=1, pady=4)
            entries.append(e)

        tk.Label(form, text="Ρόλος:").grid(row=4, column=0, sticky="w", pady=4)
        role_var = tk.StringVar(value="user")
        frm_role = tk.Frame(form)
        frm_role.grid(row=4, column=1, sticky="w")
        tk.Radiobutton(frm_role, text="User",  variable=role_var, value="user").pack(side="left")
        rb_admin = tk.Radiobutton(frm_role, text="Admin", variable=role_var, value="admin")
        rb_admin.pack(side="left")
        # Απενεργοποίηση επιλογής Admin αν υπάρχει ήδη
        if self.admin_exists():
            rb_admin.config(state="disabled")

        def do_add():
            name, email, pw, h_str = [e.get().strip() for e in entries]
            if not all([name, email, pw, h_str]):
                messagebox.showwarning("Προσοχή", "Συμπληρώστε όλα τα πεδία.", parent=win)
                return
            if self.find_user(email):
                messagebox.showerror("Σφάλμα", "Το email χρησιμοποιείται ήδη.", parent=win)
                return
            h = self.validate_hours(h_str, parent=win)
            if h is None:
                return
            role = role_var.get()
            if role == "admin" and self.admin_exists():
                messagebox.showerror("Σφάλμα", "Αδυναμία δημιουργίας 2ου Admin.", parent=win)
                return
            new_u = {"name": name, "email": email, "password": pw,
                     "hours": h, "activities": [], "role": role}
            self.users.append(new_u)
            self.save_users()
            win.destroy()
            on_success()
            messagebox.showinfo("Επιτυχία",
                                f"Ο χρήστης «{name}» ({role}) δημιουργήθηκε!",
                                parent=parent)

        tk.Button(win, text="Δημιουργία", command=do_add, width=18).pack(pady=10)

    # ── ΔΡΑΣΤΗΡΙΟΤΗΤΕΣ ────────────────────────────────────────────────────────

    def add_activity(self):
        if not self.current_user:
            return
        name = self.entry_name.get().strip()
        h_str = self.entry_hours.get().strip()
        priority = int(self.spin_priority.get())
        category = self.combo_category.get()

        if not name:
            messagebox.showwarning("Προσοχή", "Δώστε όνομα δραστηριότητας.")
            return
        h = self.validate_hours(h_str)
        if h is None:
            return

        self.current_user["activities"].append(
            {"name": name, "category": category, "time": h, "priority": priority})
        self.save_users()
        self.refresh_tree()
        self.clear_form()
        self.write_result(f"Προστέθηκε: {name}  ({category}, {h}h, ★{priority})")

    def delete_activity(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Πληροφορία", "Επιλέξτε πρώτα μια δραστηριότητα.")
            return
        idx = self.tree.index(sel[0])
        name = self.current_user["activities"][idx]["name"]
        if messagebox.askyesno("Διαγραφή", f"Να διαγραφεί η «{name}»;"):
            self.current_user["activities"].pop(idx)
            self.save_users()
            self.refresh_tree()
            self.write_result(f"Διαγράφηκε: {name}")

    def edit_activity(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Πληροφορία", "Επιλέξτε πρώτα μια δραστηριότητα.")
            return
        idx = self.tree.index(sel[0])
        act = self.current_user["activities"][idx]

        win = tk.Toplevel(self.root)
        win.title("Επεξεργασία Δραστηριότητας")
        win.resizable(False, False)
        win.grab_set()
        win.geometry("360x250")
        x = self.root.winfo_x() + (self.root.winfo_width()  - 360) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 250) // 2
        win.geometry(f"+{x}+{y}")

        tk.Label(win, text="Επεξεργασία Δραστηριότητας",
                 font=("Arial", 10, "bold")).pack(pady=10)

        form = tk.Frame(win, padx=16)
        form.pack(fill="x")

        tk.Label(form, text="Όνομα:").grid(row=0, column=0, sticky="w", pady=4)
        e_name = tk.Entry(form, width=26)
        e_name.insert(0, act["name"])
        e_name.grid(row=0, column=1, pady=4)

        tk.Label(form, text="Κατηγορία:").grid(row=1, column=0, sticky="w", pady=4)
        v_cat = tk.StringVar(value=act["category"])
        ttk.Combobox(form, textvariable=v_cat, state="readonly", width=23,
                     values=["Υποχρέωση", "Ελεύθερος Χρόνος"]).grid(row=1, column=1, pady=4)

        tk.Label(form, text="Ώρες/εβδ.:").grid(row=2, column=0, sticky="w", pady=4)
        e_hours = tk.Entry(form, width=26)
        e_hours.insert(0, str(act["time"]))
        e_hours.grid(row=2, column=1, pady=4)

        tk.Label(form, text="Σημαντικότητα (1-10):").grid(row=3, column=0, sticky="w", pady=4)
        v_prio = tk.IntVar(value=act["priority"])
        tk.Scale(form, from_=1, to=10, orient="horizontal",
                 variable=v_prio, length=180).grid(row=3, column=1, pady=4)

        def save_edit():
            name = e_name.get().strip()
            if not name:
                messagebox.showwarning("Προσοχή", "Εισάγετε όνομα.", parent=win)
                return
            h = self.validate_hours(e_hours.get().strip(), parent=win)
            if h is None:
                return
            self.current_user["activities"][idx] = {
                "name": name, "category": v_cat.get(),
                "time": h, "priority": int(v_prio.get())}
            self.save_users()
            win.destroy()
            self.refresh_tree()
            self.write_result(f"Ενημερώθηκε: {name}")

        bf = tk.Frame(win)
        bf.pack(pady=10)
        tk.Button(bf, text="Αποθήκευση", command=save_edit,   width=14).pack(side="left", padx=6)
        tk.Button(bf, text="Ακύρωση",    command=win.destroy,  width=14).pack(side="left", padx=6)

    # ── ΑΠΟΤΕΛΕΣΜΑΤΑ ──────────────────────────────────────────────────────────

    def show_optimal(self):
        if not self.current_user:
            return
        feasible, infeasible, rem = self.optimal_schedule(self.current_user)
        lines = [
            "=== ΒΕΛΤΙΣΤΟ ΕΒΔΟΜΑΔΙΑΙΟ ΠΛΑΝΟ ===\n",
            f"Διαθέσιμες ώρες : {self.current_user['hours']:.1f}h/εβδ.",
            f"Υπόλοιπο        : {rem:.1f}h\n",
            "[ ΕΦΙΚΤΕΣ ]",
        ]
        if feasible:
            for a in feasible:
                lines.append(f"  [OK] {a['name']:<22} {a['time']}h  ★{a['priority']}/10  ({a['category']})")
        else:
            lines.append("  Καμία εφικτή δραστηριότητα.")
        lines.append("\n[ ΜΗ ΕΦΙΚΤΕΣ ]")
        if infeasible:
            for a in infeasible:
                lines.append(f"  [--] {a['name']:<22} {a['time']}h  ★{a['priority']}/10  ({a['category']})")
        else:
            lines.append("  Όλες οι δραστηριότητες είναι εφικτές!")
        self.write_result("\n".join(lines))

    def show_statistics(self):
        if not self.current_user:
            return
        acts    = self.current_user["activities"]
        tasks   = [a for a in acts if a["category"] == "Υποχρέωση"]
        hobbies = [a for a in acts if a["category"] == "Ελεύθερος Χρόνος"]

        t_tot = sum(a["time"] for a in tasks)
        h_tot = sum(a["time"] for a in hobbies)
        t_avg = t_tot / len(tasks)   if tasks   else 0.0
        h_avg = h_tot / len(hobbies) if hobbies else 0.0
        total = t_tot + h_tot
        diff  = self.current_user["hours"] - total

        lines = [
            "=== ΣΤΑΤΙΣΤΙΚΑ ===\n",
            f"Χρήστης         : {self.current_user['name']}",
            f"Ρόλος           : {self.current_user.get('role', 'user')}",
            f"Διαθ. ώρες      : {self.current_user['hours']:.1f}h/εβδ.\n",
            "-- Υποχρεώσεις --",
            f"  Πλήθος        : {len(tasks)}",
            f"  Σύνολο ωρών   : {t_tot:.2f}h",
            f"  Μέσος όρος    : {t_avg:.2f}h\n",
            "-- Ελεύθερος Χρόνος --",
            f"  Πλήθος        : {len(hobbies)}",
            f"  Σύνολο ωρών   : {h_tot:.2f}h",
            f"  Μέσος όρος    : {h_avg:.2f}h\n",
            "-- Συνολικά --",
            f"  Απαιτούμενες  : {total:.2f}h",
            f"  Υπόλοιπο      : {diff:+.2f}h",
            ("  *** ΥΠΕΡΒΟΛΗ! ***" if diff < 0 else "  (Εντός ορίων)"),
        ]
        self.write_result("\n".join(lines))

    def show_chart(self):
        if not self.current_user:
            return
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
        except ImportError:
            messagebox.showwarning("Προσοχή",
                                   "Η βιβλιοθήκη matplotlib δεν είναι εγκατεστημένη.\n"
                                   "Εκτελέστε:  pip install matplotlib")
            return

        acts  = self.current_user["activities"]
        t_tot = sum(a["time"] for a in acts if a["category"] == "Υποχρέωση")
        h_tot = sum(a["time"] for a in acts if a["category"] == "Ελεύθερος Χρόνος")

        if t_tot + h_tot == 0:
            messagebox.showwarning("Προσοχή", "Δεν υπάρχουν δεδομένα για γράφημα.")
            return

        win = tk.Toplevel(self.root)
        win.title("Γραφική Αναπαράσταση")

        fig = Figure(figsize=(5, 5), dpi=100)
        ax  = fig.add_subplot(111)
        ax.pie([t_tot, h_tot],
               labels=["Υποχρεώσεις", "Ελεύθερος Χρόνος"],
               autopct="%1.1f%%")
        ax.set_title(f"Κατανομή Χρόνου — {self.current_user['name']}")
        FigureCanvasTkAgg(fig, win).get_tk_widget().pack(fill="both", expand=True)

    # ── ΑΡΧΕΙΑ ────────────────────────────────────────────────────────────────

    def save_data(self):
        if not self.current_user:
            return
        path = filedialog.asksaveasfilename(
            title="Αποθήκευση δεδομένων",
            defaultextension=".dat",
            filetypes=[("Data files", "*.dat"), ("Όλα", "*.*")],
            initialfile=f"{self.current_user['name']}_data.dat")
        if path:
            data = {"activities": self.current_user["activities"],
                    "available_hours": self.current_user["hours"]}
            with open(path, "wb") as f:
                pickle.dump(data, f)
            messagebox.showinfo("Επιτυχία", "Δεδομένα αποθηκεύτηκαν.")
            self.write_result(f"Αποθηκεύτηκε: {path}")

    def load_data(self):
        if not self.current_user:
            return
        path = filedialog.askopenfilename(
            title="Φόρτωση δεδομένων",
            filetypes=[("Data files", "*.dat"), ("Όλα", "*.*")])
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
            if messagebox.askyesno("Επιβεβαίωση", "Αντικατάσταση τρεχόντων δεδομένων;"):
                self.current_user["activities"] = data.get("activities", [])
                self.current_user["hours"]      = data.get("available_hours",
                                                           self.current_user["hours"])
                self.save_users()
                self.refresh_tree()
                self.write_result("Φόρτωση δεδομένων επιτυχής.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αδυναμία φόρτωσης:\n{e}")

    def export_dat(self):
        if not self.current_user:
            return
        path = filedialog.asksaveasfilename(
            title="Εξαγωγή δεδομένων",
            defaultextension=".dat",
            filetypes=[("Data files", "*.dat"), ("Όλα", "*.*")],
            initialfile=f"{self.current_user['name']}_data.dat")
        if path:
            with open(path, "wb") as f:
                pickle.dump(self.current_user, f)
            messagebox.showinfo("Επιτυχία", f"Εξαγωγή:\n{path}")

    def import_dat(self):
        if not self.current_user:
            return
        path = filedialog.askopenfilename(
            title="Εισαγωγή δεδομένων",
            filetypes=[("Data files", "*.dat"), ("Όλα", "*.*")])
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
            if messagebox.askyesno("Επιβεβαίωση", "Αντικατάσταση τρεχόντων δεδομένων;"):
                self.current_user["activities"] = data.get("activities", [])
                self.current_user["hours"]      = data.get("hours", self.current_user["hours"])
                self.save_users()
                self.refresh_tree()
                self.write_result("Εισαγωγή δεδομένων επιτυχής.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αδυναμία εισαγωγής:\n{e}")


# ── ΕΚΚΙΝΗΣΗ ──────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    TimeManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
