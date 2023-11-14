from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column


db = SQLAlchemy()


class Good(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    price = Column(db.Float)
    description = Column(db.Text)
    # photos will be saved as filenames inside images/ folder
    # in the single string with spaces in between
    photos = Column(db.String)

    def __init__(self, name, photos, price, description):
        self.name = name
        self.photos = photos
        self.price = price
        self.description = description


class User(db.Model):
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
    hashed_password = Column(db.String)
    # recommendations id by which the objective of the
    # recommendations algorithm will be distinguished
    rec_id = Column(db.Integer)
    # order ids will be saved as ids with spaces in between
    orders_ids = Column(db.String)

    def __init__(
            self, first_name, last_name, region, city, street_name,
            street_number, apartment_number, post_index, phone_number, email,
            hashed_password):
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
        self.orders = ""


class Order(db.Model):
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey('user.id'),
                     nullable=False)
    summ = Column(db.Float)
    # contents will be stored as goods ids with its amounts like that:
    # 'item1_id item1_amount item2_id item2_amount'
    contents = Column(db.String)
    datetime = Column(db.DateTime)

    def __init__(self, name, photos, price, description):
        self.name = name
        self.photos = photos
        self.price = price
        self.description = description
