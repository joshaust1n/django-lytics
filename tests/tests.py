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

        # create a request with the IP in META[REMOTE_ADDR]
        self.request = HttpRequest()
        self.request.method = 'GET'
        self.request.user = self.user
        self.request.META['REMOTE_ADDR'] = '127.0.0.1'

        # create a request with the IP in META[HTTP_X_FORWARDED_FOR]
        self.request2 = HttpRequest()
        self.request2.method = 'GET'
        self.request2.user = self.user
        self.request2.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.1,'
    
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

        tag2 = "event_triggered_with_everything2"
        events.register(tag2, self.request2)

        fetched_event = EventModel.objects.get(tag=tag)
        self.assertIsNotNone(fetched_event)

        fetched_event = EventModel.objects.get(tag=tag2)
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
