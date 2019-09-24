from django.test import TestCase

from .views import convert_smpte_to_frames, convert_smpte_to_ms_time


# Create your tests here.
class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        pass

    def setUp(self):
        # Set up once for every test method to setup clean data.
        pass

    def test_convert_smpte_to_ms_time(self):
        print("Method: test_convert_smpte_to_ms_time.")
        result1 = convert_smpte_to_ms_time('00:00:37:23', 24)
        result2 = convert_smpte_to_ms_time('00:00:00:01', 24)
        self.assertEquals(result1, '00:00:37,958')
        self.assertEquals(result2, '00:00:00,042')

    def test_convert_smpte_to_frames(self):
        print("Method: test_convert_smpte_to_frames.")
        result1 = convert_smpte_to_frames('01:00:00:00', 24)
        result2 = convert_smpte_to_frames('01:01:00:00', 24)
        result3 = convert_smpte_to_frames('01:01:01:00', 24)
        result4 = convert_smpte_to_frames('01:01:01:01', 24)
        self.assertEquals(result1, 86400)
        self.assertEquals(result2, 87840)
        self.assertEquals(result3, 87864)
        self.assertEquals(result4, 87865)
