import multiprocessing

bind = '0.0.0.0:8100'
workers = multiprocessing.cpu_count() * 2 + 1
forwarded_allow_ips = '*'
max_requests = 500
max_requests_jitter = 20
timeout = 120
access_log_format = '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = '/var/log/receipt_access.log'
errorlog = '/var/log/receipt_error.log'
worker_class = 'gevent'
