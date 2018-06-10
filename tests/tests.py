from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import TestCase
from django.http.request import HttpRequest
from djangolytics.models import EventModel
from djangolytics import events

class EventTestCases(TestCase):
    def setUp(self):
        self.username = "lando"
        self.password = "han is an old pirate"
        self.ip = "127.0.0.1"
        email = "lcalrissian@cloudcity.biz"

        # create a user
        self.user = User.objects.create_user(
                                            username=self.username,
                                            email=email,
                                            password=self.password
                                        )
        self.user.save()

        # create a request
        self.request = HttpRequest()
        self.request.method = 'GET'
        self.request.user = self.user
        self.request.META['REMOTE_ADDR'] = '127.0.0.1'
    
    def test_event_model_creation(self):
        tag = "event_model_creation"
        event = EventModel(
                    user=self.user,
                    ip=self.ip,
                    tag=tag
                )
        event.save()

        fetched_event = EventModel.objects.get(tag=tag)
        self.assertIsNotNone(fetched_event)
    
    def test_event_model_creation_without_user(self):
        tag = "event_model_creation_without_user"
        event = EventModel(
                    ip=self.ip,
                    tag=tag
                )
        event.save()

        fetched_event = EventModel.objects.get(tag=tag)
        self.assertIsNotNone(fetched_event)

    def test_event_triggered_with_everything(self):
        tag = "event_triggered_with_everything"
        events.register(tag, self.request)
        fetched_event = EventModel.objects.get(tag=tag)
        self.assertIsNotNone(fetched_event)
    
    def test_event_triggered_without_request(self):
        # <request> should be a required argument
        # should pass if exception raised; should fail if not raised
        with self.assertRaises(TypeError):
            tag = "event_triggered_without_request"
            events.register(tag)
            fetched_event = EventModel.objects.get(tag=tag)
            self.assertIsNotNone(fetched_event)
    
    def test_event_triggered_without_tag(self):
        # <tag> should be a required argument
        # should pass if exception raised; should fail if not raised
        with self.assertRaises(TypeError):
            tag = "event_triggered_without_tag"
            events.register(request=self.request)
            fetched_event = EventModel.objects.get(tag=tag)
            self.assertIsNotNone(fetched_event)
