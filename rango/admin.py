# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from rango.models import Page, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Page)
