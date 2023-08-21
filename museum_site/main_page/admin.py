from django.contrib import admin
from django.apps import apps

all_models = apps.get_models()

for model in all_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

from django.contrib.auth.models import User, Group, Permission
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Permission)

from django.contrib.sessions.models import Session
admin.site.unregister(Session)
