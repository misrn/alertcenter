# -*- coding: utf-8 -*-
from app import app, scheduler

if __name__ == '__main__':
    scheduler.start()
    app.run(threaded=True, host=app.config['BIND'], port=app.config['PORT'])
