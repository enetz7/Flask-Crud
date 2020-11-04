from datetime import datetime
from util.extensions import bcrypt, db
from flask_login import AnonymousUserMixin, UserMixin
# @see https://stackoverflow.com/a/37473078
class Role(UserMixin,db.Model):
    __tablename__ = 'roles'
    

    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    role = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self,role):
        """Create instance."""
        db.Model.__init__(self,role=role)
  