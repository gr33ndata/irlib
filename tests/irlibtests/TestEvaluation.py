from unittest import TestCase

from irlib.evaluation import Evaluation

class TestEvaluation(TestCase):

    def setUp(self):
        pass

    def test_correct_label_list(self):
        e = Evaluation()
        e.ev('Apples', 'Oranges')
        e.ev('Melons', 'Bananas')
        expected_labels = ['Apples', 'Oranges', 'Melons', 'Bananas']
        returned_labels = e.get_classes_labels()
        self.assertItemsEqual(returned_labels, expected_labels)


