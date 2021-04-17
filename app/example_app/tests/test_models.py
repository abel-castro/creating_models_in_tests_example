from django.test import TestCase

from example_app.tests.test_app.models import TestModel


class TestOverridingInstalledApps(TestCase):
    def setUp(self):
        self.test_model = TestModel.objects.create(
            field_a=1,
            field_b=2,
        )

    def test_objects(self):
        self.assertEqual(TestModel.objects.count(), 1)
