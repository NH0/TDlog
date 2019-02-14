from fbapp.models import User

def login_successful(POST_USERNAME, POST_PASSWORD): # Returns a boolean True if the user is in the DataBase, false otherwise
    query = User.query.filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    return result

def user_not_in_database(username):
    query = User.query.filter(User.username.in_([username]))
    result = query.first()
    return not result

def find_interests_in_db(username):
    query = User.query.filter_by(username=username).first()
    return query.interests

def find_cloud_in_db(username):
    query = User.query.filter_by(username=username).first()
    return query.wordcloud

def find_recommandation_in_db(username):
    query = User.query.filter_by(username=username).first()
    return query.recommendation

def find_cloud_path_in_db(username):
    query = User.query.filter_by(username=username).first()
    return query.cloud_path
