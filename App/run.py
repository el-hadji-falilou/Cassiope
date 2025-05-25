from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True forcé, même si FLASK_ENV n’est pas set
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
