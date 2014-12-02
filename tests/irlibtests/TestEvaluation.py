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

    def test_correct_overall_accuracy(self):
        e = Evaluation()
        e.ev('Apples' , 'Oranges')
        e.ev('Oranges', 'Oranges')
        e.ev('Apples' , 'Apples')
        e.ev('Oranges', 'Apples')
        expected_accuracy = 0.5
        returned_accuracy = e.overall_accuracy(percent=False)
        self.assertEqual(returned_accuracy, expected_accuracy)

    def test_correct_overall_fp(self):
        e = Evaluation()
        e.ev('Apples' , 'Oranges')
        e.ev('Apples' , 'Bananas')
        e.ev('Apples' , 'Apples')
        expected_fp = 2
        returned_fp = e.fp('Apples')
        self.assertEqual(returned_fp, expected_fp)

    def test_correct_overall_tp(self):
        e = Evaluation()
        e.ev('Apples' , 'Oranges')
        e.ev('Apples' , 'Apples')
        e.ev('Apples' , 'Apples')
        expected_tp = 2
        returned_tp = e.tp('Apples')
        self.assertEqual(returned_tp, expected_tp)

    def test_correct_overall_fn(self):
        e = Evaluation()
        e.ev('Apples' , 'Oranges')
        e.ev('Bananas', 'Apples')
        e.ev('Apples' , 'Apples')
        expected_fn = 1
        returned_fn = e.fn('Apples')
        self.assertEqual(returned_fn, expected_fn)

    def test_correct_overall_tn(self):
        e = Evaluation()
        e.ev('Apples' , 'Oranges')
        e.ev('Apples' , 'Apples')
        expected_tn = 0
        returned_tn = e.tn('Apples')
        self.assertEqual(returned_tn, expected_tn)


