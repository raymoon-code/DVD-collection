
from api import create_app
# from website import create_database
# from website import db

app = create_app()

if __name__ == '__main__':

    app.run(debug=True,host="127.0.0.1", PORT=5000)
