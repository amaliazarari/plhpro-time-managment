import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, pickle

# ΔΕΔΟΜΕΝΑ

DB = "usersDB.json"
users        = []   # λίστα dicts
current_user = None # dict του συνδεδεμένου χρήστη


def load_users():
    global users
    if not os.path.exists(DB):
        users = []
        return
    try:
        with open(DB, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        users = []


def save_users():
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def find_user(email, pw):
    return next((u for u in users if u["email"] == email and u["password"] == pw), None)


def optimal_schedule(user):
    """Greedy: ταξινόμηση κατά σημαντικότητα, επιλογή εντός διαθέσιμου χρόνου."""
    sorted_acts = sorted(user["activities"], key=lambda a: a["priority"], reverse=True)
    feasible, infeasible, rem = [], [], user["hours"]
    for a in sorted_acts:
        if a["time"] <= rem:
            feasible.append(a);  rem -= a["time"]
        else:
            infeasible.append(a)
    return feasible, infeasible, rem


# ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ

def clear_result():
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.config(state="disabled")


def write_result(text):
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, text)
    result_text.config(state="disabled")


def refresh_tree():
    """Ξαναγεμίζει τον πίνακα δραστηριοτήτων από τον τρέχοντα χρήστη."""
    tree.delete(*tree.get_children())
    if not current_user:
        return
    for act in current_user["activities"]:
        tree.insert("", "end", values=(
            act["name"], act["category"],
            f"{act['time']}h", f"{act['priority']}/10"))


def set_buttons_state(logged_in):
    """Ενεργοποιεί / απενεργοποιεί κουμπιά ανάλογα με σύνδεση."""
    state = "normal" if logged_in else "disabled"
    for b in buttons_need_login:
        b.config(state=state)
    btn_login.config(state="disabled" if logged_in else "normal")
    btn_logout.config(state=state)
    lbl_user.config(
        text=f"Συνδεδεμένος: {current_user['name']}" if logged_in else "Μη συνδεδεμένος"
    )


def validate_hours(val_str, parent=None):
    """Επιστρέφει float αν έγκυρο θετικό, αλλιώς εμφανίζει σφάλμα."""
    try:
        v = float(val_str)
        assert v > 0
        return v
    except Exception:
        messagebox.showerror("Σφάλμα", "Εισάγετε έγκυρο θετικό αριθμό ωρών.", parent=parent)
        return None


# ΣΥΝΔΕΣΗ / ΕΓΓΡΑΦΗ

def open_login_window():
    win = tk.Toplevel(root)
    win.title("Σύνδεση / Εγγραφή")
    win.resizable(False, False)
    win.grab_set()
    win.geometry("370x310")
    win.update_idletasks()
    x = root.winfo_x() + (root.winfo_width()  - 370) // 2
    y = root.winfo_y() + (root.winfo_height() - 310) // 2
    win.geometry(f"+{x}+{y}")

    tk.Label(win, text="Σύνδεση / Εγγραφή",
             font=("Arial", 11, "bold")).pack(pady=10)

    nb = ttk.Notebook(win)
    nb.pack(fill="both", expand=True, padx=10, pady=4)

    # Tab Σύνδεσης
    tab_l = tk.Frame(nb, padx=16, pady=12)
    nb.add(tab_l, text="  Σύνδεση  ")

    tk.Label(tab_l, text="Email:").grid(row=0, column=0, sticky="w", pady=4)
    e_email = tk.Entry(tab_l, width=28)
    e_email.grid(row=0, column=1, pady=4)

    tk.Label(tab_l, text="Κωδικός:").grid(row=1, column=0, sticky="w", pady=4)
    e_pass = tk.Entry(tab_l, width=28, show="*")
    e_pass.grid(row=1, column=1, pady=4)

    def do_login():
        global current_user
        u = find_user(e_email.get().strip(), e_pass.get())
        if u:
            current_user = u
            win.destroy()
            set_buttons_state(True)
            refresh_tree()
            write_result(f"Καλώς ήρθατε, {u['name']}!\n"
                         f"Διαθέσιμες ώρες: {u['hours']}h/εβδ.\n"
                         f"Δραστηριότητες : {len(u['activities'])}")
        else:
            messagebox.showerror("Σφάλμα", "Λανθασμένο email ή κωδικός.", parent=win)

    tk.Button(tab_l, text="Σύνδεση", command=do_login, width=20).grid(
        row=2, column=0, columnspan=2, pady=12)

    # Tab Εγγραφής
    tab_r = tk.Frame(nb, padx=16, pady=12)
    nb.add(tab_r, text="  Εγγραφή  ")

    labels_r = ["Όνομα:", "Email:", "Κωδικός:", "Ώρες/εβδ.:"]
    entries_r = []
    for i, lbl in enumerate(labels_r):
        tk.Label(tab_r, text=lbl).grid(row=i, column=0, sticky="w", pady=3)
        e = tk.Entry(tab_r, width=26, show="*" if "Κωδ" in lbl else "")
        e.grid(row=i, column=1, pady=3)
        entries_r.append(e)

    def do_register():
        global current_user
        name, email, pw, h_str = [e.get().strip() for e in entries_r]
        if not all([name, email, pw, h_str]):
            messagebox.showwarning("Προσοχή", "Συμπληρώστε όλα τα πεδία.", parent=win)
            return
        h = validate_hours(h_str, parent=win)
        if h is None:
            return
        if any(u["email"] == email for u in users):
            messagebox.showerror("Σφάλμα", "Το email χρησιμοποιείται ήδη.", parent=win)
            return
        new_u = {"name": name, "email": email, "password": pw,
                 "hours": h, "activities": []}
        users.append(new_u)
        save_users()
        current_user = new_u
        win.destroy()
        set_buttons_state(True)
        refresh_tree()
        write_result(f"Εγγραφή επιτυχής! Καλώς ήρθατε, {name}!")

    tk.Button(tab_r, text="Δημιουργία Λογαριασμού",
              command=do_register, width=24).grid(
        row=4, column=0, columnspan=2, pady=12)


def do_logout():
    global current_user
    if messagebox.askyesno("Αποσύνδεση", "Αποθήκευση & αποσύνδεση;"):
        save_users()
    current_user = None
    set_buttons_state(False)
    tree.delete(*tree.get_children())
    write_result("Αποσυνδεθήκατε.")


# ΠΡΟΣΘΗΚΗ / ΕΠΕΞΕΡΓΑΣΙΑ ΔΡΑΣΤΗΡΙΟΤΗΤΑΣ

def add_activity():
    """Προσθήκη από τη φόρμα αριστερά."""
    if not current_user:
        return
    name     = entry_name.get().strip()
    h_str    = entry_hours.get().strip()
    priority = int(spin_priority.get())
    category = combo_category.get()

    if not name:
        messagebox.showwarning("Προσοχή", "Δώστε όνομα δραστηριότητας.")
        return
    h = validate_hours(h_str)
    if h is None:
        return

    current_user["activities"].append(
        {"name": name, "category": category, "time": h, "priority": priority})
    save_users()
    refresh_tree()
    clear_form()
    write_result(f"Προστέθηκε: {name}  ({category}, {h}h, ★{priority})")


def clear_form():
    entry_name.delete(0, tk.END)
    entry_hours.delete(0, tk.END)
    spin_priority.delete(0, tk.END)
    spin_priority.insert(0, "5")


def delete_activity():
    """Διαγραφή επιλεγμένης γραμμής από τον πίνακα."""
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Πληροφορία", "Επιλέξτε πρώτα μια δραστηριότητα.")
        return
    idx  = tree.index(sel[0])
    name = current_user["activities"][idx]["name"]
    if messagebox.askyesno("Διαγραφή", f"Να διαγραφεί η «{name}»;"):
        current_user["activities"].pop(idx)
        save_users()
        refresh_tree()
        write_result(f"Διαγράφηκε: {name}")


def edit_activity():
    """Επεξεργασία επιλεγμένης δραστηριότητας σε νέο παράθυρο."""
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Πληροφορία", "Επιλέξτε πρώτα μια δραστηριότητα.")
        return
    idx = tree.index(sel[0])
    act = current_user["activities"][idx]

    win = tk.Toplevel(root)
    win.title("Επεξεργασία Δραστηριότητας")
    win.resizable(False, False)
    win.grab_set()
    win.geometry("360x250")
    x = root.winfo_x() + (root.winfo_width()  - 360) // 2
    y = root.winfo_y() + (root.winfo_height() - 250) // 2
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
                 values=["Υποχρέωση", "Ελεύθερος Χρόνος"]).grid(
                     row=1, column=1, pady=4)

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
        h = validate_hours(e_hours.get().strip(), parent=win)
        if h is None:
            return
        current_user["activities"][idx] = {
            "name": name, "category": v_cat.get(),
            "time": h, "priority": int(v_prio.get())}
        save_users()
        win.destroy()
        refresh_tree()
        write_result(f"Ενημερώθηκε: {name}")

    bf = tk.Frame(win)
    bf.pack(pady=10)
    tk.Button(bf, text="Αποθήκευση", command=save_edit, width=14).pack(side="left", padx=6)
    tk.Button(bf, text="Ακύρωση", command=win.destroy,  width=14).pack(side="left", padx=6)


# ΑΠΟΤΕΛΕΣΜΑΤΑ (εμφάνιση στο result_text)

def show_optimal():
    if not current_user:
        return
    feasible, infeasible, rem = optimal_schedule(current_user)
    lines = [
        "=== ΒΕΛΤΙΣΤΟ ΕΒΔΟΜΑΔΙΑΙΟ ΠΛΑΝΟ ===\n",
        f"Διαθέσιμες ώρες : {current_user['hours']:.1f}h/εβδ.",
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
    write_result("\n".join(lines))


def show_statistics():
    if not current_user:
        return
    acts    = current_user["activities"]
    tasks   = [a for a in acts if a["category"] == "Υποχρέωση"]
    hobbies = [a for a in acts if a["category"] == "Ελεύθερος Χρόνος"]

    t_tot = sum(a["time"] for a in tasks)
    h_tot = sum(a["time"] for a in hobbies)
    t_avg = t_tot / len(tasks)   if tasks   else 0.0
    h_avg = h_tot / len(hobbies) if hobbies else 0.0
    total = t_tot + h_tot
    diff  = current_user["hours"] - total

    lines = [
        "=== ΣΤΑΤΙΣΤΙΚΑ ===\n",
        f"Χρήστης         : {current_user['name']}",
        f"Διαθ. ώρες      : {current_user['hours']:.1f}h/εβδ.\n",
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
    write_result("\n".join(lines))


# ΓΡΑΦΗΜΑ (matplotlib — ξεχωριστό παράθυρο)

def show_chart():
    if not current_user:
        return
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
    except ImportError:
        messagebox.showwarning("Προσοχή",
            "Η βιβλιοθήκη matplotlib δεν είναι εγκατεστημένη.\n"
            "Εκτελέστε:  pip install matplotlib")
        return

    acts    = current_user["activities"]
    t_tot   = sum(a["time"] for a in acts if a["category"] == "Υποχρέωση")
    h_tot   = sum(a["time"] for a in acts if a["category"] == "Ελεύθερος Χρόνος")

    if t_tot + h_tot == 0:
        messagebox.showwarning("Προσοχή", "Δεν υπάρχουν δεδομένα για γράφημα.")
        return

    win = tk.Toplevel(root)
    win.title("Γραφική Αναπαράσταση")

    fig = Figure(figsize=(5, 5), dpi=100)
    ax  = fig.add_subplot(111)
    ax.pie([t_tot, h_tot],
           labels=["Υποχρεώσεις", "Ελεύθερος Χρόνος"],
           autopct="%1.1f%%")
    ax.set_title(f"Κατανομή Χρόνου — {current_user['name']}")

    FigureCanvasTkAgg(fig, win).get_tk_widget().pack(fill="both", expand=True)


# ΑΠΟΘΗΚΕΥΣΗ / ΦΟΡΤΩΣΗ ΔΕΔΟΜΕΝΩΝ

def save_data():
    """Αποθήκευση χρήστη σε .dat αρχείο (pickle)"""
    if not current_user:
        return
    path = filedialog.asksaveasfilename(
        title="Αποθήκευση δεδομένων",
        defaultextension=".dat",
        filetypes=[("Data files", "*.dat"), ("Όλα", "*.*")],
        initialfile=f"{current_user['name']}_data.dat")
    if path:
        data = {"activities":      current_user["activities"],
                "available_hours": current_user["hours"]}
        with open(path, "wb") as f:
            pickle.dump(data, f)
        messagebox.showinfo("Επιτυχία", "Δεδομένα αποθηκεύτηκαν.")
        write_result(f"Αποθηκεύτηκε: {path}")


def load_data():
    """Φόρτωση δεδομένων από .dat αρχείο (pickle)"""
    if not current_user:
        return
    path = filedialog.askopenfilename(
        title="Φόρτωση δεδομένων",
        filetypes=[("Data files", "*.dat"), ("Όλα", "*.*")])
    if not path:
        return
    try:
        with open(path, "rb") as f:
            data = pickle.load(f)
        if messagebox.askyesno("Επιβεβαίωση",
                               "Αντικατάσταση τρεχόντων δεδομένων;"):
            current_user["activities"] = data.get("activities", [])
            current_user["hours"]      = data.get("available_hours",
                                                   current_user["hours"])
            save_users()
            refresh_tree()
            write_result("Φόρτωση δεδομένων επιτυχής.")
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αδυναμία φόρτωσης:\n{e}")


def export_json():
    """Εξαγωγή τρέχοντος χρήστη σε JSON."""
    if not current_user:
        return
    path = filedialog.asksaveasfilename(
        title="Εξαγωγή JSON",
        defaultextension=".json",
        filetypes=[("JSON", "*.json")],
        initialfile=f"{current_user['name']}_data.json")
    if path:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Επιτυχία", f"Εξαγωγή:\n{path}")


def import_json():
    """Εισαγωγή δεδομένων χρήστη από JSON."""
    if not current_user:
        return
    path = filedialog.askopenfilename(
        title="Εισαγωγή JSON",
        filetypes=[("JSON", "*.json")])
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if messagebox.askyesno("Επιβεβαίωση",
                               "Αντικατάσταση τρεχόντων δεδομένων;"):
            current_user["activities"] = data.get("activities", [])
            current_user["hours"]      = data.get("hours", current_user["hours"])
            save_users()
            refresh_tree()
            write_result("Εισαγωγή JSON επιτυχής.")
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αδυναμία εισαγωγής:\n{e}")


# ΚΥΡΙΟ ΠΑΡΑΘΥΡΟ

load_users()

root = tk.Tk()
root.title("Project 53 - Εφαρμογή Διαχείρισης Χρόνου Υποχρεώσεων & Ελεύθερου Χρόνου")
root.geometry("1100x680")
root.minsize(900, 560)

# Τίτλος
tk.Label(root,
         text="Εφαρμογή Διαχείρισης Χρόνου Υποχρεώσεων & Ελεύθερου Χρόνου",
         font=("Arial", 14, "bold")).pack(pady=(10, 2))

lbl_user = tk.Label(root, text="Μη συνδεδεμένος", font=("Arial", 9), fg="gray")
lbl_user.pack()

# Κεντρικό frame (αριστερά + δεξιά)
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=6)

# ΑΡΙΣΤΕΡΑ — Λογαριασμός + Φόρμα καταχώρισης + Κουμπιά

left = tk.Frame(main_frame)
left.pack(side="left", fill="y", padx=(0, 8))

# Λογαριασμός
frm_account = tk.LabelFrame(left, text="Λογαριασμός", padx=8, pady=6)
frm_account.pack(fill="x", pady=(0, 6))

btn_login  = tk.Button(frm_account, text="Σύνδεση / Εγγραφή",
                        command=open_login_window, width=26)
btn_login.pack(pady=2)

btn_logout = tk.Button(frm_account, text="Αποσύνδεση",
                        command=do_logout, width=26, state="disabled")
btn_logout.pack(pady=2)

# Καταχώριση Δραστηριότητας
frm_form = tk.LabelFrame(left, text="Καταχώριση Δραστηριότητας", padx=8, pady=6)
frm_form.pack(fill="x", pady=(0, 6))

tk.Label(frm_form, text="Όνομα δραστηριότητας:").pack(anchor="w")
entry_name = tk.Entry(frm_form, width=30)
entry_name.pack(pady=(0, 4))

tk.Label(frm_form, text="Ώρες ανά εβδομάδα:").pack(anchor="w")
entry_hours = tk.Entry(frm_form, width=30)
entry_hours.pack(pady=(0, 4))

tk.Label(frm_form, text="Σημαντικότητα (1-10):").pack(anchor="w")
spin_priority = tk.Spinbox(frm_form, from_=1, to=10, width=28)
spin_priority.pack(pady=(0, 4))

tk.Label(frm_form, text="Κατηγορία:").pack(anchor="w")
combo_category = ttk.Combobox(frm_form,
                               values=["Υποχρέωση", "Ελεύθερος Χρόνος"],
                               state="readonly", width=27)
combo_category.current(0)
combo_category.pack(pady=(0, 4))

btn_add = tk.Button(frm_form, text="Προσθήκη δραστηριότητας",
                     command=add_activity, width=28, state="disabled")
btn_add.pack(pady=(4, 2))

btn_edit = tk.Button(frm_form, text="Επεξεργασία επιλεγμένης",
                      command=edit_activity, width=28, state="disabled")
btn_edit.pack(pady=2)

btn_del = tk.Button(frm_form, text="Διαγραφή επιλεγμένης",
                     command=delete_activity, width=28, state="disabled")
btn_del.pack(pady=2)

# Αποτελέσματα & Αποθήκευση
frm_actions = tk.LabelFrame(left, text="Ενέργειες", padx=8, pady=6)
frm_actions.pack(fill="x", pady=(0, 6))

btn_stats   = tk.Button(frm_actions, text="Στατιστικά",
                         command=show_statistics, width=28, state="disabled")
btn_stats.pack(pady=2)

btn_optimal = tk.Button(frm_actions, text="Βέλτιστη Διαχείριση",
                         command=show_optimal, width=28, state="disabled")
btn_optimal.pack(pady=2)

btn_chart   = tk.Button(frm_actions, text="Γράφημα",
                         command=show_chart, width=28, state="disabled")
btn_chart.pack(pady=2)

frm_files = tk.LabelFrame(left, text="Αρχεία", padx=8, pady=6)
frm_files.pack(fill="x", pady=(0, 6))

btn_save_dat = tk.Button(frm_files, text="Αποθήκευση δεδομένων (.dat)",
                          command=save_data, width=28, state="disabled")
btn_save_dat.pack(pady=2)

btn_load_dat = tk.Button(frm_files, text="Φόρτωση δεδομένων (.dat)",
                          command=load_data, width=28, state="disabled")
btn_load_dat.pack(pady=2)

btn_exp_json = tk.Button(frm_files, text="Εξαγωγή JSON",
                          command=export_json, width=28, state="disabled")
btn_exp_json.pack(pady=2)

btn_imp_json = tk.Button(frm_files, text="Εισαγωγή JSON",
                          command=import_json, width=28, state="disabled")
btn_imp_json.pack(pady=2)

tk.Button(left, text="Έξοδος", command=root.destroy,
           bg="salmon", fg="white smoke", width=28).pack(pady=4)


# ΔΕΞΙΑ — Πίνακας δραστηριοτήτων + Αποτελέσματα

right = tk.Frame(main_frame)
right.pack(side="left", fill="both", expand=True)

frm_table = tk.LabelFrame(right, text="Δραστηριότητες", padx=6, pady=4)
frm_table.pack(fill="both", expand=True)

cols = ("Δραστηριότητα", "Κατηγορία", "Ώρες/εβδ.", "Σημαντ.")
tree = ttk.Treeview(frm_table, columns=cols, show="headings", height=16)
for col in cols:
    tree.heading(col, text=col)
tree.column("Δραστηριότητα", width=220, anchor="w")
tree.column("Κατηγορία",     width=160, anchor="center")
tree.column("Ώρες/εβδ.",     width=90,  anchor="center")
tree.column("Σημαντ.",       width=80,  anchor="center")

sb_tree = ttk.Scrollbar(frm_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb_tree.set)
sb_tree.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

frm_result = tk.LabelFrame(right, text="Αποτελέσματα", padx=6, pady=4)
frm_result.pack(fill="x")

result_text = tk.Text(frm_result, height=9, font=("Courier", 9),
                       state="disabled", wrap="word",
                       relief="sunken", bd=1)
sb_res = ttk.Scrollbar(frm_result, orient="vertical", command=result_text.yview)
result_text.configure(yscrollcommand=sb_res.set)
sb_res.pack(side="right", fill="y")
result_text.pack(fill="x")


# Λίστα κουμπιών που χρειάζονται σύνδεση

buttons_need_login = [
    btn_add, btn_edit, btn_del,
    btn_stats, btn_optimal, btn_chart,
    btn_save_dat, btn_load_dat, btn_exp_json, btn_imp_json,
]

# ─────────────────────────────────────────────────────────────────────────────
write_result("Καλώς ήρθατε!\n\nΠατήστε «Σύνδεση / Εγγραφή» για να ξεκινήσετε.")
root.mainloop()
