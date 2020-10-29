from model.roles import Role
def load(db):
    for roles in [
        {'role': 'Admin'},
        {'role': 'Guest'}
    ]:
        db.session.add(Role(**roles))