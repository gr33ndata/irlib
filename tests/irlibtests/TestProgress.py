from unittest import TestCase

from irlib.progress import Progress

class TestProgress(TestCase):

    def setUp(self):
        self.p = Progress(n=1002, percent=10)

    def test_add_doc(self):
        total = 0
        for i in range(0,1002):
            total += self.p.show(message='Testing progress:', silent=True)
        self.assertEqual(total,10)   
