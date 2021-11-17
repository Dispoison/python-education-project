from flask_restx import fields

from movie_library import db, api


age_restriction_model = api.model('AgeRestriction', {
    'id': fields.Integer(readonly=True),
    'title': fields.String()
})


class AgeRestriction(db.Model):
    """Contains the properties and relationships of the
    age restriction of the movie (e.g. 16+, 18+)"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(3))
    movies = db.relationship('Movie', backref='age_restriction', lazy=True)

    def __repr__(self):
        return f'<Age restriction {self.title}>'
