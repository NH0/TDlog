from fbapp.models import User

def login_successful(POST_USERNAME, POST_PASSWORD): # Returns a boolean True if the user is in the DataBase, false otherwise
    query = User.query.filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    return result

def user_not_in_database(username):
    query = User.query.filter(User.username.in_([username]))
    result = query.first()
    return not result
