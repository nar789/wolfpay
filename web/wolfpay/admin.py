# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Shop,Product,Transaction,Send

# Register your models here.

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Send)
