import unittest

class TestPredictionRegistration(unittest.TestCase):
    def setUp(self):
        self.predictions = [
            {
                'baseline_value': '120',
                'accelerations': '0',
                'fetal_movement': '0',
                'uterine_contractions': '0',
                'light_decelerations': '0',
                'severe_decelerations': '0',
                'prolonged_decelerations': '0',
                'abnormal_variability': '73',
                'short_variability': '1',
                'percentage_of_variability': '43',
                'long_variability': '2',
                'histogram_width': '64',
                'histogram_min': '62',
                'histogram_max': '126',
                'histogram_of_peaks': '2',
                'histogram_of_zeroes': '0',
                'histogram_mode': '120',
                'histogram_mean': '137',
                'histogram_median': '121',
                'histogram_variance': '73',
                'histogram_tendency': '1'
            }
        ]

    def test_add_new_prediction(self):
        new_prediction = {
            'baseline_value': '130',
                'accelerations': '0',
                'fetal_movement': '0',
                'uterine_contractions': '0',
                'light_decelerations': '0',
                'severe_decelerations': '0',
                'prolonged_decelerations': '0',
                'abnormal_variability': '73',
                'short_variability': '1',
                'percentage_of_variability': '43',
                'long_variability': '2',
                'histogram_width': '70',
                'histogram_min': '62',
                'histogram_max': '129',
                'histogram_of_peaks': '3',
                'histogram_of_zeroes': '0',
                'histogram_mode': '120',
                'histogram_mean': '127',
                'histogram_median': '125',
                'histogram_variance': '79',
                'histogram_tendency': '1'
        }

        self.predictions.append(new_prediction)

        self.assertIn(new_prediction, self.predictions, "Expected the new prediction to be saved in the list.")

if __name__ == "__main__":
    unittest.main()
