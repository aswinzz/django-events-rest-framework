from django.shortcuts import render
# Create your views here.
from .models import Events,Occurrences
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.decorators import (api_view,
                                       permission_classes,
                                       throttle_classes,)
from rest_framework.response import Response
from .serializers import EventSerializer,OccurrencesSerializer
from datetime import datetime, timedelta
from .week import week_of_month

class EventApi(APIView):
    def get(self,request,format=None):
        if request.GET.get('start'):
            start = request.GET.get('start')
        else:
            start="2017-01-01"
        if request.GET.get('end'):
            end=request.GET.get('end')
        else:
            end="2020-01-01"
        events=Occurrences.objects.filter(start__gt=start,end__lt=end)
        serializer = OccurrencesSerializer(events,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,format=None):
        date_format = "%Y-%m-%d"
        title=request.data.get('title')
        repeats=request.data.get('repeats')
        repeat_frequency=request.data.get('repeat_frequency')
        end_date=request.data.get('end_date')
        start_date=request.data.get('start_date')
        start_time=request.data.get('start_time')
        end_time=request.data.get('end_time')
        dow=None
        if(request.data.get('dow')):
            dow=request.data.get('dow')
        week_type=None
        if(request.data.get('week_type')):
            week_type=request.data.get('week_type')
        data={
            'title':title,
            'start_date':start_date,
            'end_time':request.data.get('end_time'),
            'start_time':request.data.get('start_time'),
            'description':request.data.get('description'),
            'category':request.data.get('category'),
            'end_date':end_date,
            'experience':request.data.get('experience'),
            'available_to':request.data.get('available_to'),
            'venue_location':request.data.get('venue_location'),
            'venue_alternate':request.data.get('venue_alternate'),
            'repeat_frequency':repeat_frequency,
            'repeats':repeats,
            'week_type':week_type,
            'dow':dow,
            'venue_type':request.data.get('venue_type'),
            'subcategories':request.data.get('subcategories')
        }
        event=Events(event=data)
        event.save()
        start=start_date+' '+start_time
        end=start_date+' '+end_time
        data={
                'event':event,
                'start':start,
                'end':end,
                'title':title
        }
        if(request.data.get('repeats')==0):
            occurrence=Occurrences(**data)
            occurrence.save()
        else:
            new_start = datetime.strptime(start_date, date_format)
            new_end = datetime.strptime(end_date, date_format)
            no_days=(new_end - new_start).days
            if repeat_frequency==1:
                occurrence=None
                for i in range(0,no_days):
                    temp_start=new_start.strftime('%Y-%m-%d')
                    temp_start_DT=temp_start+' '+start_time
                    temp_end_DT=temp_start+' '+end_time
                    data={
                                'event':event,
                                'start':temp_start_DT,
                                'end':temp_end_DT,
                                'title':title
                        }
                    new_start+=timedelta(days=1)
                    occurrence=Occurrences(**data)
                    occurrence.save()
                    occurrence=None
            elif repeat_frequency==2:
                occurrence=None
                dow=request.data.get('dow')
                for d in dow:
                    new_start = datetime.strptime(start_date, date_format)
                    new_end = datetime.strptime(end_date, date_format)
                    while(new_start<=new_end):
                        if new_start.isoweekday()==d:
                            temp_start=new_start.strftime('%Y-%m-%d')
                            temp_start_DT=temp_start+' '+start_time
                            temp_end_DT=temp_start+' '+end_time
                            data={
                                        'event':event,
                                        'start':temp_start_DT,
                                        'end':temp_end_DT,
                                        'title':title
                                }
                            occurrence=Occurrences(**data)
                            occurrence.save()
                            occurrence=None
                            new_start+=timedelta(days=7)
                        else:
                            new_start+=timedelta(days=1)

            elif repeat_frequency==3:
                occurrence=None
                dow=request.data.get('dow')
                week_type=request.data.get('week_type')
                new_start = datetime.strptime(start_date, date_format)
                new_end = datetime.strptime(end_date, date_format)
                while(new_start<=new_end):
                    if week_type==week_of_month(new_start):
                        if new_start.isoweekday() in dow:
                            temp_start=new_start.strftime('%Y-%m-%d')
                            temp_start_DT=temp_start+' '+start_time
                            temp_end_DT=temp_start+' '+end_time
                            data={
                                    'event':event,
                                    'start':temp_start_DT,
                                    'end':temp_end_DT,
                                    'title':title
                                }
                            occurrence=Occurrences(**data)
                            occurrence.save()
                            occurrence=None
                    new_start+=timedelta(days=1)
        eventserializer = EventSerializer(event)
        return Response(eventserializer.data, status=status.HTTP_200_OK)
