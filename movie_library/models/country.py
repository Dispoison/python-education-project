from flask_restx import fields

from movie_library import db, api


country_model = api.model('Country', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(default='Country'),
    'abbreviation': fields.String(default='CT')
})


class Country(db.Model):
    """Contains the properties and relationships of the country"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    abbreviation = db.Column(db.String(2))
    movies = db.relationship('Movie', backref='country', lazy=True)

    def __repr__(self):
        return f'<Country {self.title} ({self.abbreviation})>'
