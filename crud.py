from model import db, User, Progress

def create_user(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def user_progress(user_id):
    return Progress.query.filter_by(user_id=user_id).all()

def update_progress(user_id, collectible_name, collected):
    progress = Progress.query.filter_by(user_id=user_id, collectible_name=collectible_name).first()
    if progress:
        progress.collected = collected
        db.session.commit()
        print("Updating progress for user:", user_id)
        return True
    else:
        new_progress = Progress(user_id=user_id, collectible_name=collectible_name, collected=collected)
        db.session.add(new_progress)
        db.session.commit()
        print("Creating progress for user:", user_id)
        return True 

def reset_user_progress(user_id):
    progress = Progress.query.filter_by(user_id=user_id).all()
    for item in progress:
        db.session.delete(item)
    db.session.commit()
    return True
