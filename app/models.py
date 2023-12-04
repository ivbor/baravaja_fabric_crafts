"""
Database initialization
"""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime


db = SQLAlchemy()


class Good(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    price = Column(db.Float)
    description = Column(db.Text)
    # photos will be saved as filenames inside images/ folder
    # in the single string with spaces in between
    photos = Column(db.String)

    def __init__(self,
                 name: str | None = None,
                 photos: str | None = None,
                 price: float | None = None,
                 description: str | None = None):
        self.name = name
        self.photos = photos
        self.price = price
        self.description = description


class User(UserMixin, db.Model):
    id = Column(db.Integer, primary_key=True)
    first_name = Column(db.String)
    last_name = Column(db.String)
    street_name = Column(db.String)
    street_number = Column(db.Integer)
    apt_number = Column(db.Integer)
    city = Column(db.String)
    region = Column(db.String)
    post_index = Column(db.String)
    phone_num = Column(db.String)
    email = Column(db.String, unique=True)
    # password = Column(db.String)
    hashed_password = Column(db.String)
    # recommendations id by which the objective of the
    # recommendations algorithm will be distinguished
    rec_id = Column(db.Integer)
    # order ids will be saved as ids with spaces in between
    orders_ids = Column(db.String)
    is_admin = Column(db.Boolean, default=False)

    def __init__(self, email: str,
                 hashed_password: str,
                 first_name: str | None = None,
                 last_name: str | None = None,
                 region: str | None = None,
                 city: str | None = None,
                 street_name: str | None = None,
                 street_number: int | None = None,
                 apartment_number: int | None = None,
                 post_index: str | None = None,
                 phone_number: str | None = None,
                 rec_id: int | None = None,
                 orders_ids: str | None = None,
                 is_admin: bool = False):
        self.first_name = first_name
        self.last_name = last_name
        self.region = region
        self.city = city
        self.street_name = street_name
        self.street_number = street_number
        self.apartment_number = apartment_number
        self.post_index = post_index
        self.phone_number = phone_number
        self.email = email
        self.hashed_password = hashed_password
        self.orders_ids = orders_ids
        self.rec_id = rec_id
        self.is_admin = is_admin


class Order(db.Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey('user.id'),
                     nullable=False)
    summ = Column(db.Float)
    # contents will be stored as goods ids with its amounts like that:
    # 'item1_id item1_amount item2_id item2_amount'
    contents = Column(db.String)
    datetime = Column(db.DateTime)

    def __init__(self,
                 user_id: int | None = None,
                 summ: float | None = None,
                 contents: str | None = None,
                 datetime: DateTime | None = None):
        self.user_id = user_id
        self.summ = summ
        self.contents = contents
        self.datetime = datetime
