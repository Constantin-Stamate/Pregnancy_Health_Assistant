import unittest

class TestRetrieveLastPrediction(unittest.TestCase):
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

    def test_get_last_prediction(self):
        def get_last_prediction(predictions):
            if predictions: 
                return predictions[-1]
            return None

        new_prediction = {
            'baseline_value': '140',
            'accelerations': '1',
            'fetal_movement': '1',
            'uterine_contractions': '1',
            'light_decelerations': '1',
            'severe_decelerations': '0',
            'prolonged_decelerations': '0',
            'abnormal_variability': '80',
            'short_variability': '2',
            'percentage_of_variability': '50',
            'long_variability': '3',
            'histogram_width': '75',
            'histogram_min': '65',
            'histogram_max': '135',
            'histogram_of_peaks': '4',
            'histogram_of_zeroes': '1',
            'histogram_mode': '125',
            'histogram_mean': '135',
            'histogram_median': '130',
            'histogram_variance': '85',
            'histogram_tendency': '1'
        }
        self.predictions.append(new_prediction)

        last_prediction = get_last_prediction(self.predictions)

        self.assertEqual(last_prediction, new_prediction, "Expected the last prediction to be returned without removal.")

if __name__ == "__main__":
    unittest.main()
