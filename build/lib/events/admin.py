from django.contrib import admin
from .models import Events,Occurrences

admin.site.register(Events,verbose_name="Events")
admin.site.register(Occurrences,verbose_name="Occurrences")