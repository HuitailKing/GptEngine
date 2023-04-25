from django.test import TestCase

class MyViewTestCase(TestCase):
    def test_my_view(self):
        response = self.client.get('/my-view-url/?param1=value1&param2=value2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'param1=value1')
        self.assertContains(response, 'param2=value2')