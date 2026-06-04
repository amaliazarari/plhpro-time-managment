import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "GUI"))
from GUI.GUI_finalC import main
from methods.fileMethods import *
from services.authUser import (find_user, create_user, authenticate_user, delete_user, admin_exists)
from services.activityService import (add_activity, remove_activity, edit_activity, list_activities)

# --- Κύριο Μενού ---
def main():
    # Η τοπική λίστα που θα κρατάει τα δεδομένα μας κατά την εκτέλεση
    role_choice=0
    read_log_file = 'usersDB.txt'
    users = read_users(read_log_file)
    print("Users loaded: ", users)

    # Αν δεν υπάρχουν καθόλου χρήστες, δημιουργία πρώτου Admin
    if not users:
        print("\nΔεν υπάρχουν χρήστες στο σύστημα.")
        print("Δημιουργία πρώτου Admin:")
        name = input("Όνομα: ")
        email = input("email: ")
        password = input("password: ")
        new_user = create_user(users, name, email, password, "admin")
        write_users("usersDB.txt", users)
        print("Ο πρώτος Admin δημιουργήθηκε με επιτυχία!")

    while True:
        print("\n=== MENOY ΔΙΑΧΕΙΡΙΣΗΣ ΧΡΟΝΟΥ ===")
        print("1. Σύνδεση")
        print("2. Εκτύπωση Δεδομένων")
        print("3. Exit")

        choice = input("Επιλογή: ")

        if choice == '1':
            email = input("email: ")
            password = input("password: ")

            # Έλεγχος εισόδου χρήστη
            current_user = authenticate_user(users, email, password)

            if current_user is None:
                print("Λάθος email ή password")
            else:
                print(f"Καλώς ήρθες {current_user.name}")

                #Έλεγχος για admin ή user
                if current_user.role == "admin":
                    # καλούμε ξεχωριστή συνάρτηση για τον admin
                    admin_menu(current_user, users)
                else:
                    user_menu(current_user, users)
        # if choice == '1':
        #     sign_in_choice = input("a. Για εισαγωγή νέων χρηστών: \nb. Σύνδεση χρήστη: \nc. Διαγραφή χρήστη: \n")
        #     if sign_in_choice == 'a':
        #         name = input("Όνομα: ")
        #         email = input("email: ")
        #
        #         #Έλεγχος αν το email που πληκτρολογήθηκε είναι μοναδικό
        #         while find_user(users, email) is not None:
        #             print("Το email χρησιμοποιείται ήδη!! ")
        #             email = input("Δώσε άλλο email: ")
        #
        #         password = input("password: ")
        #
        #         """Ελέγχουμε αν υπάρχει ήδη χρήστης ή οχι. Αν δεν υπάρχει χρήστης, ο πρώτος δηλαδή που θα κάνει
        #            εγγραφή θα έχει και την επιλογή admin και την επιλογή user. Εάν υπάρχει ήδη χρήστης admin τότε δεν
        #            θα μπορούμε να ξαναδηλώσουμε admin θα μπορούμε να δηλώνουμε μόνο users"""
        #         print("1.Admin")
        #         print("2.User")
        #         role_choice = input("Επιλογή Ρόλου: ")
        #
        #         #Επιλογή ρόλου
        #         while role_choice == '1' and admin_exists(users):
        #             print("Αδυναμία δημιουργίας 2ου admin")
        #             role_choice = input("Δώσε νέο ρόλο (1.Admin/2.User): ")
        #
        #         if role_choice == '1':
        #             role = "admin"
        #             print("Ο νέος χρήστης δημιουργήθηκε ως admin")
        #
        #         if role_choice == '2':
        #             role = "user"
        #             print("Ο νέος χρήστης δημιουργήθηκε ως user")
        #
        #         """Οι παρακάτω 2 γραμμές αφαιρέθηκαν για τις δοκιμές, αλλά δεν τις έχω διαγράψει
        #            μήπως και τις χρειαστούμε ξανά"""
        #
        #         # προσθήκη νέου χρήστη στήν λίστα.
        #         new_user = create_user(users, name, email, password, role)
        #
        #
        #         if new_user is None:
        #             print("Το email χρησιμοποιείται ήδη")
        #         else:
        #             write_users("usersDB.txt", users)
        #             print("Συγχαρητήρια!\nΝέος χρήστης προστέθηκε με επιτυχία")
        #     elif sign_in_choice == 'b':
        #         email = input("email: ")
        #         password = input("password: ")
        #
        #         #Έλεγχος εισόδου χρήστη
        #         current_user = authenticate_user(users, email, password)
        #
        #         if current_user is None:
        #             print("Λάθος email ή password")
        #         else:
        #             print(f"Καλώς ήρθες {current_user.name}")
        #
        #             #Έλεγχος για admin ή user
        #             if current_user.role == "admin":
        #                 print("ADMIN MENU")
        #             else:
        #                 print("USER MENU")
        #
        #             print("Συνδεθήκατε")
        #             user_menu(current_user, users)
        #
        #     elif sign_in_choice == 'c':
        #         print("Διαδικασία Διαγραφής Χρήστη:")
        #     else:
        #         print("Ops!\nΠληκτρολόγησες δεδομένα :( \nΞαναπροσπάθησε")

        elif    choice == '2':
            print("\n ---Αποθηκευμένοι Χρήστες---")
            for user in users:
                print(user)

        elif choice == '3':
            #write_users("usersDB.txt", users)
            print("Έξοδος...")
            break
        else:
            print("Λάθος επιλογή, προσπαθήστε ξανά.")

def admin_menu(current_user, users):
    while True:
        print(f"\n=== ΜΕΝΟΥ ADMIN {current_user.name} ===")
        print("1. Προσθήκη Χρήστη")
        print("2. Διαγραφή Χρήστη")
        print("3. Προσθήκη δραστηριότητας")
        print("4. Διαγραφή δραστηριότητας")
        print("5. Επεξεργασία δραστηριοτήτων")
        print("6. Εμφάνιση δραστηριοτήτων")
        print("7. Αποσύνδεση")

        choice = input("Επιλογή: ")

        if choice == '1':
            name = input("Όνομα: ")
            email = input("email: ")

            # Έλεγχος αν το email που πληκτρολογήθηκε είναι μοναδικό
            while find_user(users, email) is not None:
                print("Το email χρησιμοποιείται ήδη!! ")
                email = input("Δώσε άλλο email: ")
            """Ελέγχουμε αν υπάρχει ήδη χρήστης ή οχι. Αν δεν υπάρχει χρήστης, ο πρώτος δηλαδή που θα κάνει
                           εγγραφή θα έχει και την επιλογή admin και την επιλογή user. Εάν υπάρχει ήδη χρήστης admin τότε δεν
                           θα μπορούμε να ξαναδηλώσουμε admin θα μπορούμε να δηλώνουμε μόνο users"""

            password = input("password: ")

            print("1.Admin")
            print("2.User")
            role_choice = input("Επιλογή Ρόλου: ")

            # Επιλογή ρόλου
            while role_choice == '1' and admin_exists(users):
                print("Αδυναμία δημιουργίας 2ου admin")
                role_choice = input("Δώσε νέο ρόλο (1.Admin/2.User): ")

            if role_choice == '1':
                role = "admin"
                print("Ο νέος χρήστης δημιουργήθηκε ως admin")

            if role_choice == '2':
                role = "user"
                print("Ο νέος χρήστης δημιουργήθηκε ως user")

            """Οι παρακάτω 2 γραμμές αφαιρέθηκαν για τις δοκιμές, αλλά δεν τις έχω διαγράψει
               μήπως και τις χρειαστούμε ξανά"""

            # προσθήκη νέου χρήστη στήν λίστα.
            new_user = create_user(users, name, email, password, role)

            if new_user is None:
                print("Το email χρησιμοποιείται ήδη")
            else:
                write_users("usersDB.txt", users)
                print("Συγχαρητήρια!\nΝέος χρήστης προστέθηκε με επιτυχία")

            # # Έλεγχος εισόδου χρήστη
            # current_user = authenticate_user(users, email, password)
            #
            # if current_user is None:
            #     print("Λάθος email ή password")
            # else:
            #     print(f"Καλώς ήρθες {current_user.name}")
            #
            #     # Έλεγχος για admin ή user
            #     if current_user.role == "admin":
            #         # καλούμε ξεχωριστή συνάρτηση για τον admin
            #         admin_menu(current_user, users)
            #     else:
            #         user_menu(current_user, users)
# """"""
# while True:
#     sign_in_choice = input("a. Για εισαγωγή νέων χρηστών: \nb. Σύνδεση χρήστη: \nc. Διαγραφή χρήστη: \n")
#     if sign_in_choice == 'a':
#         name = input("Όνομα: ")
#         email = input("email: ")
#
#         # Έλεγχος αν το email που πληκτρολογήθηκε είναι μοναδικό
#         while find_user(users, email) is not None:
#             print("Το email χρησιμοποιείται ήδη!! ")
#             email = input("Δώσε άλλο email: ")
#
#         password = input("password: ")



        # elif choice == '2':
        #     email = input("email: ")
        #     password = input("password: ")
        #
        #     # Έλεγχος εισόδου χρήστη
        #     current_user = authenticate_user(users, email, password)
        #
        #     if current_user is None:
        #         print("Λάθος email ή password")
        #     else:
        #         print(f"Καλώς ήρθες {current_user.name}")
        #
        #         # Έλεγχος για admin ή user
        #         if current_user.role == "admin":
        #             print("ADMIN MENU")
        #         else:
        #             print("USER MENU")
        #
        #         print("Συνδεθήκατε")
        #         user_menu(current_user, users)

        elif choice == '2':
            print("Διαδικασία Διαγραφής Χρήστη:")
        # else:
        #     print("Ops!\nΠληκτρολόγησες δεδομένα :( \nΞαναπροσπάθησε")


        # Προσθήκη δραστηριότητας
        elif choice == '3':
            print("\n-- Προσθήκη Δραστηριότητας --")
            print("1. Υποχρέωση(Task)")
            print("2. Δραστηριότητας (Hobbie)")
            type_choice = input("Επιλογή τύπου: ")

            if type_choice == '1':
                acticity_type = "task"
            elif type_choice == '2':
                acticity_type = "hobbie"
            else:
                print("Λάθος Επιλογή!!")

                continue
            # Όνομα δραστηριότητας
            name = input("'Ονομα δραστηριότητας: ")

            # Διαθέσιμος χρόνος
            time = float(input("Διαθέσιμος χρόνος: "))
            while time <= 0:
                print("Ο χρόνος πρέπει να είναι μεγαλύτερος του 0!")
                time = float(input("Διαθέσιμος χρόνος: "))

            # Δήλωση Προτεραιότητας
            priority = int(input("Προτεραιότητα (1-10): "))
            while priority < 1 or priority > 10:
                print("Η προτεραιότητα πρέπει να είναι μεταξύ 1 και 10!")
                priority = int(input("Προτεραιότητα (1-10): "))

            result = add_activity(current_user, acticity_type, name, time, priority)

            if result:
                write_users("usersDB.txt", users)
                print(f"H δραστηριότητα '{name}' προστέθηκε επιτυχώς!")
            else:
                print("Λάθος τύπος δραστηριότητας")


        # Διαγραφή δραστηριότητας
        elif choice == '4':
            print("--Διαγραφή Δραστηριότητας--")
            print("1. Υποχρέωση (Task)")
            print("2. Δραστηρίοτητα (Hobbie)")
            type_choice = input("Επιλογή τύπου:")

            if type_choice == '1':
                acticity_type = 'task'
            elif type_choice == '2':
                acticity_type = 'hobbie'
            else:
                print("Λάθος επιλογή.")
                continue

            name = input("Όνομα δραστηριότητας προς διαγραφή: ")
            result = remove_activity(current_user, acticity_type, name)

            if result:
                write_users("usersDB.txt", users)
                print(f"Η δραστηριότητα '{name}' διαγράφηκε επιτυχώς!")
            else:
                print(f"Δεν διαγράφηκε δραστηριότητα με όνομα '{name}'.")

        # Επεξεργασία δραστηριότητας
        elif choice == '5':
            print("\n-- Επεξεργασία Δραστηριότητας --")
            print("1. Υποχρέωση (Task)")
            print("2. Δραστηριότητα (Hobbie)")
            type_choice = input("Επιλογή τύπου: ")

            if type_choice == '1':
                acticity_type = "task"
            elif type_choice == '2':
                acticity_type = "hobbie"
            else:
                print("Λάθος επιλογή.")
                continue

            name = input("Όνομα δραστηριότητας προς επεξεργασία: ")
            print("(Πάτα Enter αν δεν θέλεις να αλλάξεις κάτι)")
            new_name = input("Νέο όνομα: ") or None
            new_time = input("Νέες ώρες: ") or None
            new_priority = input("Νέα προτεραιότητα: ") or None

            if new_time is not None:
                new_time = float(new_time)
            if new_priority is not None:
                new_priority = int(new_priority)

            result = edit_activity(current_user, acticity_type, name, new_name, new_time, new_priority)

            if result:
                write_users("usersDB.txt", users)
                print(f"Η δραστηριότητα '{name}' ενημερώθηκε επιτυχώς!")
            else:
                print(f"Δεν βρέθηκε δραστηριότητα με όνομα '{name}'.")

        # Εμφάνιση δραστηριοτήτων
        elif choice == '6':
            list_activities(current_user)

        # Αποσύνδεση
        elif choice == '7':
            print(f"Αποσύνδεση χρήστη {current_user.name}. Αντίο!!!")
            break
        else:
            print("Λάθος επιλογή, προσπάθησε ξανά.")


def user_menu(current_user, users):

    type_choice=0
    while True:
        print(f"\n=== ΜΕΝΟΥ ΧΡΗΣΤΗ{current_user.name} ===")
        print("1. Προσθήκη δραστηριότητας")
        print("2. Διαγραφή δραστηριότητας")
        print("3. Επεξεργασία δραστηριοτήτων")
        print("4. Εμφάνιση δραστηριοτήτων")
        print("5. Αποσύνδεση")

        choice = input("Επιλογή: ")

        #Προσθήκη δραστηριότητας
        if choice == '1':
            print("\n-- Προσθήκη Δραστηριότητας --")
            print("1. Υποχρέωση(Task)")
            print("2. Δραστηριότητας (Hobbie)")
            type_choice=input("Επιλογή τύπου: ")

            if type_choice == '1':
                acticity_type = "task"
            elif type_choice == '2':
                acticity_type = "hobbie"
            else:
                print("Λάθος Επιλογή!!")

                continue
            #Όνομα δραστηριότητας
            name= input("'Ονομα δραστηριότητας: ")

            #Διαθέσιμος χρόνος
            time = float(input("Διαθέσιμος χρόνος: "))
            while time<=0:
                print("Ο χρόνος πρέπει να είναι μεγαλύτερος του 0!")
                time = float(input("Διαθέσιμος χρόνος: "))

            #Δήλωση Προτεραιότητας
            priority=int(input("Προτεραιότητα (1-10): "))
            while priority<1 or priority>10:
                print("Η προτεραιότητα πρέπει να είναι μεταξύ 1 και 10!")
                priority = int(input("Προτεραιότητα (1-10): "))

            result=add_activity(current_user, acticity_type, name, time, priority)

            if result:
                write_users("usersDB.txt", users)
                print(f"H δραστηριότητα '{name}' προστέθηκε επιτυχώς!")
            else:
                print("Λάθος τύπος δραστηριότητας")


        #Διαγραφή δραστηριότητας
        elif choice == '2':
            print("--Διαγραφή Δραστηριότητας--")
            print("1. Υποχρέωση (Task)")
            print("2. Δραστηρίοτητα (Hobbie)")
            type_choice=input("Επιλογή τύπου:")

            if type_choice == '1':
                acticity_type = 'task'
            elif type_choice == '2':
                acticity_type = 'hobbie'
            else:
                print("Λάθος επιλογή.")
                continue

            name=input("Όνομα δραστηριότητας προς διαγραφή: ")
            result=remove_activity(current_user, acticity_type, name)

            if result:
                write_users("usersDB.txt", users)
                print(f"Η δραστηριότητα '{name}' διαγράφηκε επιτυχώς!")
            else:
                print(f"Δεν διαγράφηκε δραστηριότητα με όνομα '{name}'.")

        #Επεξεργασία δραστηριότητας
        elif choice == '3':
            print("\n-- Επεξεργασία Δραστηριότητας --")
            print("1. Υποχρέωση (Task)")
            print("2. Δραστηριότητα (Hobbie)")
            type_choice=input("Επιλογή τύπου: ")

            if type_choice == '1':
                acticity_type = "task"
            elif type_choice == '2':
                acticity_type = "hobbie"
            else:
                print("Λάθος επιλογή.")
                continue

            name=input("Όνομα δραστηριότητας προς επεξεργασία: ")
            print("(Πάτα Enter αν δεν θέλεις να αλλάξεις κάτι)")
            new_name=input("Νέο όνομα: ") or None
            new_time=input("Νέες ώρες: ") or None
            new_priority=input("Νέα προτεραιότητα: ") or None

            if new_time is not None:
                new_time=float(new_time)
            if new_priority is not None:
                new_priority=int(new_priority)

            result=edit_activity(current_user, acticity_type, name, new_name, new_time, new_priority)

            if result:
                write_users("usersDB.txt", users)
                print(f"Η δραστηριότητα '{name}' ενημερώθηκε επιτυχώς!")
            else:
                print(f"Δεν βρέθηκε δραστηριότητα με όνομα '{name}'.")

        #Εμφάνιση δραστηριοτήτων
        elif choice == '4':
            list_activities(current_user)

        #Αποσύνδεση
        elif choice == '5':
            print(f"Αποσύνδεση χρήστη {current_user.name}. Αντίο!!!")
            break
        # else:
        #     print("Λάθος επιλογή, προσπάθησε ξανά.")


if __name__ == "__main__":
    main()