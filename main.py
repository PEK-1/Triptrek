from waitress import serve
from wbsite import create_app

app= create_app()

if __name__ == '__main__':
    serve(app)
    