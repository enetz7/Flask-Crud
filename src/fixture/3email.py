from model.email import Email
def load(db):
    for email in [
        {'email': 'endika.ph99@gmail.com'},
        {'email': 'probar@gmail.com'}
    ]:
        db.session.add(Email(**email))