# Η κλάση αυτή περιγράφει τον χρήστη
class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.tasks=[]
        self.hobbies = []

    #Για πιο εύκολη εκτύπωση
    def __str__(self):
        return (f"User Name: {self.name},email: {self.email},Password: {self.password}, Role:{self.role},")
