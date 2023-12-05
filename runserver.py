from waitress import serve
from pos.wsgi import application
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

if __name__ == '__main__':
    serve(application, host="127.0.0.1", port='8080')
