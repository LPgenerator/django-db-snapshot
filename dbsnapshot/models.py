# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models
from dbsnapshot import defaults, client


class Server(models.Model):
    host = models.IPAddressField(_('Remote ip'))
    port = models.PositiveIntegerField(
        _('Remote port'), default=defaults.SERVER_PORT)
    days = models.PositiveIntegerField(
        _('Clean after'), help_text=_('on days'), default=7)
    per_day = models.PositiveIntegerField(_('Max backups per day'), default=6)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(
        _('Updated'), auto_now=True, auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True)

    class Meta:
        verbose_name = _('Server')
        verbose_name_plural = _('Servers')

    def __unicode__(self):
        return self.host

    def __execute(self, method, status=True, *args):
        try:
            cli = client.Client(self.host, self.port)
            cli.send(method, *args)
            result = cli.recv()
            cli.close()
            return result['status'] if status is True else result
        except Exception, msg:
            if hasattr(self, 'raise_exc') and self.raise_exc:
                raise
            print '[dbsnapshot]', msg.__unicode__()

    def remote_clean(self):
        return self.__execute('cleanup')

    def remote_backup(self):
        return self.__execute('backup')

    def remote_status(self):
        return self.__execute('status')

    remote_status.short_description = _('Replica status')
    remote_status.boolean = True

    def remote_hello(self):
        return self.__execute('hello')

    def remote_delete(self, filename):
        return self.__execute('delete', True, filename)

    def remote_list(self):
        bak_list = self.__execute('list', status=False)
        if bak_list:
            bak_list.remove('lost+found')
        return bak_list

    def remote_list_num(self):
        bak_list = self.remote_list()
        return bak_list and len(bak_list) or 0

    remote_list_num.short_description = _('Number of backups')

    def __sync_crontab(self, key, task, period):
        from djcelery.models import PeriodicTask, IntervalSchedule

        old = self.pk and self._default_manager.get(pk=self.pk)
        if old is None or getattr(old, key) != getattr(self, key):
            task = PeriodicTask.objects.get_or_create(
                name='DB Snapshot: %s' % task,
                task='dbsnapshot.tasks.%s' % task,
                enabled=True
            )[0]

            every = int(86400.0 / getattr(self, key))
            if period == 'days':
                every = getattr(self, key)

            if not task.interval:
                task.interval = IntervalSchedule.objects.get_or_create(
                    every=every, period=period)[0]
            else:
                task.interval.every = every
                task.interval.save()
            task.save()

    def save(self, *args, **kwargs):
        self.__sync_crontab('per_day', 'create_snapshot', 'seconds')
        self.__sync_crontab('days', 'remove_old_snapshots', 'days')
        super(Server, self).save(*args, **kwargs)


class Log(models.Model):
    server = models.ForeignKey(Server, verbose_name=_('Remote server'))
    date = models.DateField(_('Date'), auto_now=True)
    start = models.DateTimeField(_('Started'), )
    end = models.DateTimeField(_('Finished'), auto_now=True)
    elapsed = models.FloatField(_('Elapsed'))
    success = models.BooleanField(default=False)
    method = models.PositiveIntegerField(choices=(
        (1, _('backup')),
        (2, _('clean'))
    ))

    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')
        ordering = ('-id',)

    def __unicode__(self):
        return self.server.host
