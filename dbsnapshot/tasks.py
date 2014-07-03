# -*- coding: utf-8 -*-

from django.utils.timezone import now
from dbsnapshot import models
from celery.task import task
from time import time


class LogOperation(object):
    def __init__(self, server, method):
        self.server = server
        self.method = method
        self.start_time = None
        self.start_date = None

    def __enter__(self):
        self.server.raise_exc = 1
        self.start_time = time()
        self.start_date = now()

    def __exit__(self, *args):
        return models.Log.objects.create(
            server=self.server,
            start=self.start_date,
            elapsed="%0.2f" % (time() - self.start_time),
            success=not all(args),
            method=self.method
        )


def _task(method, method_num):
    for server in models.Server.objects.filter(status=True):
        with LogOperation(server, method_num):
            getattr(server, method)()


@task
def create_snapshot():
    _task('remote_backup', 1)


@task
def remove_old_snapshots():
    _task('remote_clean', 2)
