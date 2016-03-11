# -*- coding: utf-8 -*-
from django.contrib import admin
from general.models import Document, People


class PeopleAdmin(admin.ModelAdmin):
    filter_horizontal = ('documents', )


admin.site.register(Document)
admin.site.register(People, PeopleAdmin)
