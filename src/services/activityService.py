from models.activity import Hobbie, Task


def add_activity(user, activity_type, name, time, priority):
    """Συνάρτηση η οποία προσθέτει νέα δραστηριότητα στον χρήστη.
       Επιστρέφει το νεο activity object αν το type ειναι λάθος"""
    if activity_type == "task":
        new_activity = Task(time, priority, name)
        user.tasks.append(new_activity)
        return new_activity
    elif activity_type == "hobbie":
        new_activity = Hobbie(time, priority, name)
        user.hobbies.append(new_activity)
        return new_activity

    return None


def find_activity(user, activity_type, name):
    """Συνάρτηση η οποία ψάχνει activity με βάση το όνομα
       Επιστρέφει το activity object ή None αν δεν βρει"""
    if activity_type == "task":
        for activity in user.tasks:
            if activity.name == name:
                return activity
    elif activity_type == "hobbie":
        for activity in user.hobbies:
            if activity.name == name:
                return activity

    return None


def remove_activity(user, activity_type, name):
    """Συνάρτηση η οποία αφαιρεί δραστηριότητα από το χρήστη με βάση το όνομα
       Επιστρέφει True αν διαγράφηκε, False αν δεν βρέθηκε"""
    activity = find_activity(user, activity_type, name)

    if activity is None  :
        return False

    if activity_type == "task":
        user.tasks.remove(activity)
    elif activity_type == "hobbie":
        user.hobbies.remove(activity)

    return True


def edit_activity(user, activity_type, name, new_name, new_time, new_priority):
    """Συνάρτηση η οποία επεξεργάζεται υπάρχον activity.
       Επιστρέφει True αν άλλαξε, False αν δεν βρέθηκε activity"""

    #Θέτουμε None για τις νεες τιμές(new_time, new_name, new_priority)
    new_name=None
    new_time=None
    new_priority=None

    activity = find_activity(user, activity_type, name)

    if activity is None:
        return False

    if new_name is not None:
        activity.edit_name(new_name)

    if new_time is not None:
        activity.edit_time(new_time)

    if new_priority is not None:
        activity.edit_priority(new_priority)

    return True

def list_activities(user):
    """Εκτυπώνει όλες τις δραστηριότητες του χρήστη"""
    print(f"\n--- Υποχρεώσεις (Tasks) του {user.name} ---")
    if not user.tasks:
        print("Δεν υπάρχουν υποχρεώσεις")
    else:
        for i, task in enumerate(user.tasks, 1):
            print(f"{i}. {task.name}")

    print(f"\n--- Δραστηριότητες (Hobbies) του {user.name} ---")
    if not user.hobbies:
        print("Δεν υπάρχουν δραστηριότητες.")
    else:
        for i, hobbie in enumerate(user.hobbies, 1):
            print(f"{i}. {hobbie}")


    #Σύνολο ωρών
    total_tasks = sum(task.time for task in user.tasks)
    total_hobbies = sum(hobbie.time for hobbie in user.hobbies)
    print(f"\n Συνολικές ώρες υποχρεώσεων: {total_tasks}h")
    print(f"\n Συνολικές ώρες δραστηριοτήτων: {total_hobbies}h")




