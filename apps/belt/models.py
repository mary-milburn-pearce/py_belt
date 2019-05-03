from django.db import models
from apps.login.models import Person
import datetime

class EventManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # try:
        if len(postData['dest']) < 3:
            errors["dest"] = "Destination must consist of at least 3 characters"
        if len(postData['start_dt']) < 1:
            errors["start"] = "Start Date cannot be blank"
        if len(postData['end_dt']) < 1:
            errors["end"] = "End Date cannot be blank"
        if len(postData['plan']) < 3:
            errors["plan"] = "Plan must consist of at least 3 characters"
        else:
            d1 = datetime.datetime.strptime(postData['start_dt'], "%Y-%m-%d").date()
            d2 = datetime.datetime.strptime(postData['end_dt'], "%Y-%m-%d").date()
            print("Date range:", d1, d2)
            if d1 < datetime.datetime.now().date():
                errors["future"] = "Event must be in the future (time travel is not currently supported)"
            elif d1 > d2:
                errors["dates"] = "End date must follow start date (time travel is not currently supported)"
        # except:
            # errors["unhandled"] = "Data input could not be validated. Please check that date formats are correct."
        return errors

class Event(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=255)
    organizer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="hosted_events")
    attendees = models.ManyToManyField(Person, related_name="attending_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=EventManager()

    def __repr__(self):
        return f"Dest: {self.destination}, Starts: {self.start_date}, \
                    Ends: {self.end_date}, Plan: {self.plan}"
