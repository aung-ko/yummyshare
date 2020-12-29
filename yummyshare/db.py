from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from click import command, echo
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

# local imports
from . import login_manager


# Initialize SQLAlchemy
db = SQLAlchemy()

CUISINES = [('american', 'American Cuisine'), ('european', 'European Cuisine'),
            ('asian', 'Asian Cuisine'), ('latina', 'Latina Cuisine'), ('other', 'Other')]
COURSES = [
    ('appetizers-snacks', 'Appetizers and Snacks'),
    ('breads', 'Bread'),
    ('desserts', 'Desserts'),
    ('drink', 'Drinks'),
    ('main-dish', 'Main Dishes'),
    ('salad', 'Salad'),
    ('side-dishes', 'Side Dishes'),
    ('soups-stews-chili', 'Soups, Stews and Chili'),
    ('breakfast-brunch', 'Breakfast and Brunch'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('fruits-vegetables', 'Fruits, Vegetables and Other Produce'),
    ('meat-poultry', 'Meat and Poultry'),
    ('pasta-noodles', 'Pasta and Noodles'),
    ('seafood', 'Seafood'),
    ('bbq', ' BBQ & Grilling'),
    ('other', 'Other')
]

# users_saved_recipes = db.Table('users_saved_recipes',
#                                db.Column('user_id', db.Integer,
#                                          db.ForeignKey('users.id')),
#                                db.Column('recipe_id', db.Integer,
#                                          db.ForeignKey('recipes.id'))
#                                )

users_saved_recipes = db.Table('users_saved_recipes',
                               db.Column('recipe_id', db.Integer, db.ForeignKey(
                                   'recipes.id'), primary_key=True),
                               db.Column('user_id', db.Integer, db.ForeignKey(
                                   'users.id'), primary_key=True)
                               )


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')
    # saved_recipes = db.relationship('Recipe',
    #                                 secondary=users_saved_recipes)
    saved_recipes = db.relationship('Recipe', secondary=users_saved_recipes, lazy='subquery',
                                    backref=db.backref('users', lazy=True))
    is_admin = db.Column(db.Boolean, default=False)
    created_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Recipe(db.Model):
    """
    Create a Recipe table
    """

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    cuisine = db.Column(db.String(50))
    course = db.Column(db.String(100))
    description = db.Column(db.String(255))
    image = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Recipe: {}>'.format(self.name)

    @property
    def display_cuisine(self):
        """
        Show cuisine in readable form.
        """
        for cuisine in CUISINES:
            if self.cuisine == cuisine[0]:
                return cuisine[1]
        return ''

    @property
    def display_course(self):
        """
        Show course in readable form.
        """
        for course in COURSES:
            if self.course == course[0]:
                return course[1]
        return ''


@command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    echo("Initialized the database.")


def init_app(app):
    """Initialize the Flask app for database usage."""
    db.init_app(app)
    app.cli.add_command(init_db_command)
