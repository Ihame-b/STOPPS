"""
WSGI config for ecomproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import json
import traceback
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')

# #region agent log
try:
    log_path = Path(__file__).parent.parent / '.cursor' / 'debug.log'
    with open(log_path, 'a') as f:
        f.write(json.dumps({
            'sessionId': 'debug-session',
            'runId': 'wsgi-init',
            'hypothesisId': 'E',
            'location': 'wsgi.py:20',
            'message': 'WSGI application initializing',
            'data': {'settings_module': os.environ.get('DJANGO_SETTINGS_MODULE')},
            'timestamp': int(__import__('time').time() * 1000)
        }) + '\n')
except Exception:
    pass
# #endregion

try:
    application = get_wsgi_application()
    # #region agent log
    try:
        log_path = Path(__file__).parent.parent / '.cursor' / 'debug.log'
        with open(log_path, 'a') as f:
            f.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'wsgi-init',
                'hypothesisId': 'E',
                'location': 'wsgi.py:35',
                'message': 'WSGI application created successfully',
                'data': {},
                'timestamp': int(__import__('time').time() * 1000)
            }) + '\n')
    except Exception:
        pass
    # #endregion
except Exception as e:
    # #region agent log
    try:
        log_path = Path(__file__).parent.parent / '.cursor' / 'debug.log'
        with open(log_path, 'a') as f:
            f.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'wsgi-init',
                'hypothesisId': 'E',
                'location': 'wsgi.py:45',
                'message': 'WSGI application creation failed',
                'data': {
                    'error': str(e),
                    'traceback': traceback.format_exc()
                },
                'timestamp': int(__import__('time').time() * 1000)
            }) + '\n')
    except Exception:
        pass
    # #endregion
    raise
