from website import create_app
# from website import create_database
# from website import db

app = create_app()

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     print('Database created')
    app.run(debug=True)