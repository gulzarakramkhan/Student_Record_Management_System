import json

from django.db import models


class AnyValue(models.Field):
    description = "A field that stores arbitrary Python values as JSON text"

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop("max", None)
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return "text"

    def get_internal_type(self):
        return "TextField"

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None or value == "":
            return None

        if isinstance(value, (dict, list, tuple, set, int, float, bool, type(None))):
            return value

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        if isinstance(value, str):
            try:
                return json.loads(value)
            except (TypeError, ValueError):
                return value

        return value

    def get_prep_value(self, value):
        if value is None:
            return None
        return json.dumps(value, default=str)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return "" if value is None else json.dumps(value, default=str)


# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=30, null=True)
    username = models.CharField(max_length=12, unique=True, null=True)
    password = models.CharField(max_length=30, unique=True, null=True)
    college = models.CharField(max_length=50, null=True)
    city_name = models.CharField(max_length=20, null=True)
    Joining_Date = models.DateField(null=True)
    Total_fee = AnyValue(null=True)
    Paid_fee = AnyValue(null=True)
    left_fee = AnyValue(null=True)
    phone = AnyValue(max=10, null=True)
    Technology = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='student_images/',null=True,blank=True)
    



