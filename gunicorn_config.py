# The configuration file for gunicorn when used on server.

# Bind gunicorn to port 8000.
bind = '0.0.0.0:8000'

# Set three workers.
workers = 3

# Log paths to log to when errors are encountered.
accesslog = '/var/log/gunicorn.access.log'
errorlog = '/var/log/gunicorn.error.log'