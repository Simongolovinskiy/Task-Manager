from task_manage import create_app, database



app = create_app()


if __name__ == '__main__':
    with app.app_context():
        database.create_all()
        app.run(debug=False, port=8080, host='0.0.0.0')
    
