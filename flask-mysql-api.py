from configparser import ConfigParser
import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(f'{dir_path}/flask-mysql-api.cfg')
logging.basicConfig(filename=config['LOG']['FILE'], level=config['LOG']['LEVEL'])


if __name__ == '__main__':
    logging.error("test")