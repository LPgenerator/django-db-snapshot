# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.shortcuts import redirect
from django.contrib import admin
from dbsnapshot import models


class ServerAdmin(admin.ModelAdmin):
    list_display = (
        'host', 'port', 'status', 'remote_status', 'remote_list_num',
        'days', 'per_day', 'created', 'updated', 'actions_column', 'id',)
    search_fields = ('host',)
    list_filter = ('status', 'created', 'updated',)

    def __init__(self, *args, **kwargs):
        super(ServerAdmin, self).__init__(*args, **kwargs)
        self._col_inst = None

    def _get_link(self, title, view_name):
        return '[<a href="%s">%s</a>] ' % (
            reverse('admin:%s' % view_name, args=(self._col_inst.pk,),
                    current_app=self.admin_site.name),
            unicode(title)
        )

    def actions_column(self, instance, actions=''):
        self._col_inst = instance
        actions += self._get_link(_('backup'), 'backup_view')
        actions += self._get_link(_('clean'), 'clean_view')
        actions += self._get_link(_('list of backups'), 'backup_list')
        return actions

    actions_column.short_description = _('Actions')
    actions_column.allow_tags = True

    def _server_view(self, request, pk, template, extra_context=None):
        context = {
            'server': models.Server.objects.get(pk=pk),
            'app_label': models.Server._meta.app_label,
            'verbose_name': unicode(models.Server._meta.verbose_name),
        }
        if extra_context is not None:
            context.update(extra_context)
        return TemplateResponse(
            request, 'dbsnapshot/admin/%s.html' % template, context,
            current_app=self.admin_site.name)

    def backup_view(self, request, pk):
        return self._server_view(request, pk, 'backup_view')

    def clean_view(self, request, pk):
        return self._server_view(request, pk, 'clean_view')

    def backup_list_view(self, request, pk):
        return self._server_view(request, pk, 'backup_list')

    def backup_delete_view(self, request, pk, filename):
        models.Server.objects.get(pk=pk).remote_delete(filename)
        return redirect(
            reverse(
                'admin:backup_list', args=(pk,),
                current_app=self.admin_site.name
            )
        )

    def get_urls(self):
        urls = super(ServerAdmin, self).get_urls()

        admin_urls = patterns(
            '',
            url(
                r'^backup/(\d+)/$',
                self.admin_site.admin_view(self.backup_view),
                name='backup_view'
            ),
            url(
                r'^backup/clean/(\d+)/$',
                self.admin_site.admin_view(self.clean_view),
                name='clean_view'
            ),
            url(
                r'^backup/list/(\d+)/$',
                self.admin_site.admin_view(self.backup_list_view),
                name='backup_list'
            ),
            url(
                r'^backup/delete/(\d+)/(.*?)/$',
                self.admin_site.admin_view(self.backup_delete_view),
                name='backup_delete'
            ),
        )
        return admin_urls + urls


class BackupLogAdmin(admin.ModelAdmin):
    list_display = (
        'server', 'method', 'start', 'end', 'elapsed',
        'success', 'date', 'id',)
    date_hierarchy = 'date'
    search_fields = ('server__host',)
    list_filter = ('method', 'success', 'date',)

    def __init__(self, model, admin_site):
        super(BackupLogAdmin, self).__init__(model, admin_site)

        self.readonly_fields = [field.name for field in model._meta.fields]
        self.readonly_model = model

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return request.method != 'POST'


admin.site.register(models.Server, ServerAdmin)
admin.site.register(models.Log, BackupLogAdmin)
