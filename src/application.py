from models.user import User
from models.activity import Hobbie,Task
from methods.fileMethods import *

#τεστ ότι δουλεύουν οι κλάσεις και οι συναρτήσεις
def app():
    user1=User(name="Amalia", email="std170663@ac.eap.gr", password="pass123$", role="admin", our_spend_activities=[8], our_spend_hobbies=[8])
    print(user1)

    hobbie1 = Hobbie(2, 5, "tennis")
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

    while True:
        print("\n=== MENOY ΔΙΑΧΕΙΡΙΣΗΣ ΧΡΟΝΟΥ ===")
        print("1. Σύνδεση")
        print("2. Προβολή χρηστών")
        print("3. Exit")

        choice = input("Επιλογή: ")

        if choice == '1':
            sign_in_choice = input("a. Για εισαγωγή νέων χρηστών: \nb. Σύνδεση χρήστη:\n")
            if sign_in_choice == 'a':
                name = input("Όνομα: ")
                email = input("email: ")
                password = input("password: ")
                role = input("role: ")
                our_spend_activities = input("Εκτιμώμενος χρόνος υποχρεώσεων σε ώρες: ")
                our_spend_hobbies = input("Εκτιμώμενος χρόνος δραστηριοτήτων σε ώρες: ")
                # προσθήκη νέου χρήστη στήν λίστα.
                users.append(User(name, email, password, role, our_spend_activities, our_spend_hobbies))
                print("Συγχαρητήρια!\nΝέος χρήστης προστέθηκε με επιτυχία")
                write_users("usersDB.txt", users)

            elif sign_in_choice == 'b':
                email = input("email: ")
                password = input("password: ")
                print("Συνδεθήκατε")

            else:
                print("Ops!\nΠληκτρολόγησες δεδομένα :( \nΞαναπροσπάθησε")

        elif choice == '2':
            view_user_choice = input("a. Για προβολή χρηστών: \nb. Για πλήθος χρηστών:\n")
            if view_user_choice == 'a':
                print("--Διαθέσιμοι χρήστες--\n")
                for user in users:
                    print(f"{user.name} {user.role}")
                    # print(user.name + " " + user.role) Κάνει το ίδιο με το πάνω
            elif view_user_choice == 'b':
                print(f"{len(users)} καταγεγραμμένοι χρήστες")
            else:
                print("Ops!\nΠληκτρολόγησες δεδομένα :( \nΞαναπροσπάθησε")

        elif choice == '3':
            write_users("usersDB.txt", users)
            print("Έξοδος...")
            break
        else:
            print("Λάθος επιλογή, προσπαθήστε ξανά.")

if __name__ == "__main__":
    app() #τεστ ότι δουλεύουν οι κλάσεις και οι συναρτήσεις
    main() # --- Κύριο Μενού ---