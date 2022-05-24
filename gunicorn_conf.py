bind = ["0.0.0.0:80"]
backlog = 512
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 300
graceful_timeout = 2
limit_request_field_size = 8192
