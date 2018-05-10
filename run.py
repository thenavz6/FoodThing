from routes import app

if __name__ == '__main__':
    app.run(host='localhost', port=5000, ssl_context=('cert.pem', 'key.pem'), debug = True)
