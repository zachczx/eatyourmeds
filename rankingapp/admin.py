from django.contrib import admin
from .models import Worker, Session, Sequence

# Register your models here.

admin.site.register(Worker)
admin.site.register(Session)
admin.site.register(Sequence)