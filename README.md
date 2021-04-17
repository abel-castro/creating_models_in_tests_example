# Create and use Django Models in Test Cases

Let's image we need a new model only for a test case. We can create something similar than this:

**example_app.tests.test_app.models.TestModel**

```python
from django.db import models


class TestModel(models.Model):
    field_a = models.IntegerField()
    field_b = models.IntegerField()

    class Meta:
        app_label = 'test_app'
```

We could try to use `TestModel` and create objects in a test case:
**test_models.py**

```python
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
```

But if you run the tests like this, the test will fail and return DB errors like these:

**./manage.py test**

```
django.db.utils.ProgrammingError: relation "test_app_testmodel" does not exist
LINE 1: INSERT INTO "test_app_testmodel" ("field_a", "field_b") VALU...
```

It fails because Django needs to have `TestModel` registered in INSTALLED_APPS. We do not really want to add our `example_app.tests.test_app` to INSTALLED_APPS because we only need it when we run the tests. 

The solution is to to add the test_app to the settings with [modify_settings](https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.SimpleTestCase.modify_settings) and calling migrate.

**test_models.py**

```python
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
```

## Run the tests
- Create a .env file from the template env_template_dev with the desired values.
- Run the tests
```
docker-composer run --rm django /app/manage.py test
```
