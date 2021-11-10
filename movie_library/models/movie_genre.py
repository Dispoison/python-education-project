from movie_library import db

movie_genre = db.Table('movie_genre',
                       db.Column('movie_id', db.Integer,
                                 db.ForeignKey('movie.id'), primary_key=True),
                       db.Column('genre_id', db.Integer,
                                 db.ForeignKey('genre.id'), primary_key=True))
