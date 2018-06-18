from rest_framework import serializers
from datetime import datetime
from .models import Events,Occurrences


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id','event')

class OccurrencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrences
        fields = ('__all__')
        depth=1