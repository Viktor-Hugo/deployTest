from waitress import serve
from pybo import create_app

app = create_app()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
