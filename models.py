from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class User(db.Model):
    __tablename__ = "users"

    # username
    username = db.Column(db.Text, primary_key = True, nullable=False, unique=True)
    # password
    password = db.Column(db.Text, nullable=False)
    # "profile" pic 
    image_url = db.Column(db.Text, nullable=False, default="/static/images/default-pic.png")

    favorites = db.relationship("Favorite", cascade="all, delete", backref="user")

    @classmethod
    def register(cls, username, password, image_url):
        """Register user info with hashed password"""
        # hash a password before storing it in the databse
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        # now the "hashed" variable is utf-8 encoded and can be stored in our database easier. 

        # return a new user instance
        return cls(username=username, password=hashed_utf8, image_url=image_url)
    
    @classmethod
    def authenticate(cls, username, password):
        """Authenticatiopn for username and password at login"""
        # find the first username with the username entered
        user = User.query.filter_by(username=username).first()
         # make sure the passwords and username match in order to login. return the user. otherwise return false
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Favorite(db.Model):
    __tablename__ = "favorites"

    # create an ID column
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    # create a username column
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
    # the game id so you can store it 
    game_id = db.Column(db.Integer, nullable=False)
    # name of teh game
    name = db.Column(db.Text, nullable=False)
    # image
    background_image = db.Column(db.Text)