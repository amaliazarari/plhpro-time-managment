# Η κλάση αυτή περιγράφει τον χρήστη
class User:
    def __init__(self, name, email, password, role, hours):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.hours = hours
        self.activities = []
        self.tasks=[]
        self.hobbies = []

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)

    #Για πιο εύκολη εκτύπωση
    def __str__(self):
        return (f"User Name: {self.name},email: {self.email},Password: {self.password}, Role:{self.role},")
