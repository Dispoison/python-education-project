"""Project launch point"""

from movie_library import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run()
