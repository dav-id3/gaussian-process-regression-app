"""gunicorn config file"""

import os

# server Socket
bind = f'0.0.0.0:{os.environ.get("API_PORT", 8000)}'

# Worker Processes
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 300

# access log
accesslog = "-"

# error log
erroring = "-"
