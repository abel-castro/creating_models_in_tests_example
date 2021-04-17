from django.db import models


class TestModel(models.Model):
    field_a = models.IntegerField()
    field_b = models.IntegerField()

    class Meta:
        app_label = 'test_app'
