from django.db import models
from django.contrib.postgres.fields import JSONField
class Events(models.Model):
    event=JSONField(null=True,blank=True)
    class Meta:
        verbose_name_plural = "Events"
    def __str__(self):
        return 'title: '+self.event.get('title')+' - type : '+str(self.event.get('repeat_frequency'))

    def __unicode__(self):
        return 'title: '+self.event.get('title')+' - type : '+str(self.event.get('repeat_frequency'))

class Occurrences(models.Model):
    event=models.ForeignKey(Events,on_delete=models.CASCADE)
    start=models.DateTimeField(blank=False, null=False)
    end=models.DateTimeField(blank=False, null=False)
    title=models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Occurrences"
    def __str__(self):
        return 'title: '+self.title+' - '+'parent: '+str(self.event.id)

    def __unicode__(self):
        return 'title: '+self.title+' - '+'parent: '+str(self.event.id)