import sys
from routes import app

if sys.version_info[0] < 3:
    raise Exception("Must use python3. Try 'python3 run.py'")
    exit()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, ssl_context=('cert.pem', 'key.pem'), debug = True)
