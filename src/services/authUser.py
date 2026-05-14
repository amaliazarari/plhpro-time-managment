from models.user import User

#Η συνάρτηση "find_user" αυτή ψάχνει έναν χρήστη με βάση το email του.
#Αν το βρει επιστρέφει το αντικείμενο User
#Αν δεν το βρει επιστρέφει None
def find_user(users, email):

    for user in users:
        if user.email == email:   #Αν βρούμε ίδιο email με ένα χρήστη επιστρέφουμε το χρήστη
            return user

    return None


def authenticate_user(users, email, password):
    user = find_user(users, email)

    if user is None:                      #Αν δεν βρεθηκε χρήστης επιστρέφουμε None
        return None

    if user.password == password:         #Αν βρεθεί χρήστης και το password είναι σωστό τότε επιστρέφουμε το χρήστη
        return user

    return None


def create_user(users, name, email, password, role, available_hours, activities):
    existing_user = find_user(users, email)

    if existing_user is not None:
        return None

    new_user = User(name, email, password, role, available_hours, activities)

    users.append(new_user)
    return new_user


def delete_user(users, email):
    user=find_user(username,password)

    if user is None:
        return False

    users.remove(user)

    return True
