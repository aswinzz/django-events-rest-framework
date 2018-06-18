Django Events for Django Rest Framework
========

Package for scheduling events with easy integration with fullcalendar using Django Rest Framework

Information
========

* [Documentation](django-events-rest-framework.readthedocs.io)


Installation
========

```bash
pip install django-events-rest-framework
```

Edit your `settings.py`

Add to `INSTALLED_APPS`:

```python
'events',
```

Features
========

 * one-time,daily,weekly and monthly recurring events
 * easy integration with [fullcalendar](fullcalendar.io)
 * Endpoints for creating an event and viewing events during a specific period
 * ready to use, events package

 Reccurring Events
 ========
 ## One time
 The Occurrence object is created once for the given date and time

 ## daily
 Occurrence object will be created for all the days in between `start_date` and `end_date`

 ## weekly
 User can select days of week in which the event will repeat , this will be done for all the weeks till the `end_recurring_date`

## monthly
In this type , the user can select which week of a month (`week_type`) and which days (`dow`) of the week to repeat the events

Configuration
========

GET REQUEST
========

Endpoint : `http://127.0.0.1:8000/events/event?start="start_date"&end="end_date` 
This endpoint returns all the events in between `start_date` and `end_date`.
To integrate with fullcalendar this endpoint can be used as a json feed for events.

POST REQUEST
========

Endpoint : `http://127.0.0.1:8000/events/event` 
This endpoint creates events according to the type of events.For all the reccurring events an occurrence object is create in the Occurrences table.
POST data must contain :
* title : Some name for the event
* start_date : Starting date of the event
* start_time : Starting time of the event
* end_time : ending time of the event
* end_recurring_date : if the event is reccurring then this date will be used as a limiting end_recurring_date
* repeats : 0 - if the event occurs only once , 1 if the event is reccurring
* repeat_frequenct : 0 - if the event occurs only once, 1 if for daily ,2 for weekly ,3 for monthly
* dow : An array for days of week in which the event occurs ( only for weekly and monthly ) . Example : `[1,4,5]`
* week_type : only for monthly ( 0:first week of the month ,1:second week of the month ...)

