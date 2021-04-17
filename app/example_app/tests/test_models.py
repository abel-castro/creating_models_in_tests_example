from django.core.management import call_command
from django.test import TestCase, modify_settings

from example_app.tests.test_app.models import TestModel


@modify_settings(INSTALLED_APPS={
    'append': 'example_app.tests.test_app',
})
class TestOverridingInstalledApps(TestCase):
    def setUp(self):
        call_command('migrate', run_syncdb=True)
        self.test_model = TestModel.objects.create(
            field_a=1,
            field_b=2,
        )

    def test_objects(self):
        self.assertEqual(TestModel.objects.count(), 1)
