from classes.user import User
from classes.activity import Hobbie,Task
from methods.fileMethods import *

#τεστ ότι δουλεύουν οι κλάσεις και οι συναρτήσεις
def app():
    user1 = User("Amalia", "std170663@ac.eap.gr", "pass123$", 8, 8)
    print(user1)

    hobbie1 = Hobbie(30, 5, "tennis")
    print(hobbie1)

    hobbie1.edit_time(5)
    print(hobbie1)

    task1 = Task(5, 9, "job")
    print(task1)

    task1.edit_priority(7)
    print(task1)

# --- Κύριο Μενού ---
def main():
    # Η τοπική λίστα που θα κρατάει τα δεδομένα μας κατά την εκτέλεση
    read_log_file = 'usersDB.txt'
    users = read_users(read_log_file)
    print(users)


    while True:
        print("\n=== MENOY ΔΙΑΧΕΙΡΙΣΗΣ ΧΡΟΝΟΥ ===")
        print("1. Εισαγωγή Δεδομένων")
        print("2. Exit")

        choice = input("Επιλογή: ")

        if choice == '1':
            sign_in_choice = input("a. Για εισαγωγή νέων χρηστών: \nb. Σύνδεση χρήστη:\n")
            if sign_in_choice == 'a':
                name = input("Όνομα: ")
                email = input("email: ")
                password = input("password: ")
                our_spend_activities = input("Εκτιμώμενος χρόνος υποχρεώσεων σε ώρες: ")
                our_spend_hobbies = input("Εκτιμώμενος χρόνος δραστηριοτήτων σε ώρες: ")
                # προσθήκη νέου χρήστη στήν λίστα.
                users.append(User(name, email, password, our_spend_activities, our_spend_hobbies))
                print("Συγχαρητήρια!\nΝέος χρήστης προστέθηκε με επιτυχία")
            elif sign_in_choice == 'b':
                print("--Διαθέσιμοι χρήστες--\n")
                email = input("email: ")
                password = input("password: ")
                print("Συνδεθήκατε")
            else:
                print("Ops!\nΠληκτρολόγησες δεδομένα :( \nΞαναπροσπάθησε")

        elif choice == '2':
            write_users("usersDB.txt", users)
            print("Έξοδος...")
            break
        else:
            print("Λάθος επιλογή, προσπαθήστε ξανά.")

if __name__ == "__main__":
    app() #τεστ ότι δουλεύουν οι κλάσεις και οι συναρτήσεις
    main() # --- Κύριο Μενού ---