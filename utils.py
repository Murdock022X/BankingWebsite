from models import Messages

def get_messages(username):
    return Messages.query.filter_by(username=username)
