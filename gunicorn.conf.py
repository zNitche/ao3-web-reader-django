import multiprocessing


bind = "0.0.0.0:8000"

workers = 2 * multiprocessing.cpu_count() + 1
threads = multiprocessing.cpu_count()
worker_class = "gthread"

timeout = 10
keepalive = 5
