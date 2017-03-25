import gevent.monkey
gevent.monkey.patch_all()

# import multiprocessing

debug = False
loglevel = 'notice'
bind = '0.0.0.0:5000'
pidfile = '/var/run/gunicorn/app.pid'
logfile = '/var/log/gunicorn/app.log'

# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
