# config/logging_config.py
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/sistema_arriendos.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errores.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'formatter': 'detailed',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {  # Logger raíz
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': True
        },
        'conex.conn': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False
        }
    }
}