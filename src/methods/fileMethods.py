import pickle as pkl

def write_users(file_name, users):
    with open(file_name, "wb" ) as f:
        f.write(pkl.dumps(users))

def read_users(file_name):
    try:
        with open(file_name , "rb") as f:
            users = pkl.loads(f.read())
        return users
    except FileNotFoundError:
        return []