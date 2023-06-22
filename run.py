from task_manage import create_app, database



app = create_app()


if __name__ == '__main__':
    with app.app_context():
        #database.drop_all()
        database.create_all()
        app.run(debug=True, port=5000)
    
