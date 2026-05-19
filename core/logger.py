import logging
import logging.handlers
import os

def setup_logging(app):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    handler = logging.handlers.RotatingFileHandler(
        'logs/app.log', maxBytes=1024*1024, backupCount=5)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] %(message)s'))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
