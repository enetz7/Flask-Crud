from model.user import User
def load(db):
    for user in [
        {'first_name': 'Endika', 'last_name': 'Hernandez',
         'postal_code': '20304', 'username': 'Endibra90','password': '123456789','country':'Guipuzkoa','locality':'Valencia','address':'Bertsolari','phone_number':'682512971'},
        {'first_name': 'Willi', 'last_name': 'Rex',
         'postal_code': '20305', 'username': 'Willi','password': '123456789','country':'Araba','locality':'Irun','address':'Antaño','phone_number':'682612743'}
    ]:
        db.session.add(User(**user))