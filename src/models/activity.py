# Η κλάση αυτή περιγράφει τον χρήστη
class Activity:
    def __init__(self, time, priority, name):
        self.time = time
        self.priority = priority
        self.name = name

    #Για πιο εύκολη εκτύπωση
    def __str__(self):
        return f" Name: {self.name}, Time: {self.time},Priority: {self.priority}"

    #Συναρτήσεις για επεξεργασία χρόνου, προτεραιότητας και ονόματος για τα Activity
    def edit_time(self, new_time):
        self.time = new_time

    def edit_priority(self, new_priority):
        self.priority = new_priority

    def edit_name(self, new_name):
        self.name = new_name

  #  def array_task_list(self, name):

class Hobbie(Activity):
    def __init__(self, time, priority, name):
        super().__init__(time, priority, name)
        self.mandatory = False

class Task(Activity):
    def __init__(self, time, priority, name):
        super().__init__(time, priority, name)
        self.mandatory = True

