# logging_config.py
import logging
import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',  # You can change this to 'DEBUG' in dev
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',  # You can change this to 'INFO' in production
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
