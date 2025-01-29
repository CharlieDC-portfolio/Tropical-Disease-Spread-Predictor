import unittest
import io
import os

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_reg_predict_all_valid(self):
        form = {
            'province': 'An Giang',
            'predStartDate': '2017-01',
            'predEndDate': '2017-12',
            'diseases': 'Dengue_fever'
        }
        response = self.client.post('/predictReg', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        self.assertEqual(response_json['Error'], False)

    def test_reg_predict_province_null(self):
        form = {
            'province': ' ',
            'predStartDate': '2017-01',
            'predEndDate': '2017-12',
            'diseases': 'Dengue_fever'
        }
        response = self.client.post('/predictReg', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_reg_predict_start_null(self):
        form = {
            'province': 'An Giang',
            'predStartDate': '',
            'predEndDate': '2017-12',
            'diseases': 'Dengue_fever'
        }
        response = self.client.post('/predictReg', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_reg_predict_end_null(self):
        form = {
            'province': 'An Giang',
            'predStartDate': '2017-01',
            'predEndDate': '',
            'diseases': 'Dengue_fever'
        }
        response = self.client.post('/predictReg', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_reg_predict_disease_null(self):
        form = {
            'province': 'An Giang',
            'predStartDate': '2017-01',
            'predEndDate': '2017-12',
            'diseases': ''
        }
        response = self.client.post('/predictReg', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)
        
    def test_reg_predict_end_before_start(self):
        form = {
            'province': 'An Giang',
            'predStartDate': '2017-12',
            'predEndDate': '2017-01',
            'diseases': 'Dengue_fever'
        }
        response = self.client.post('/predictReg', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Ensure Start Date preceeds End Date"}
        self.assertEqual(response_json, expected_json)

    def test_xtreme_predict_all_valid_within_checked(self):

        with open('TestFile.csv', 'rb') as f:
            form = {
                'within': 'on',
                'timeframe': 2,
                'file': f
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": False,"msg": "The Ensemble model predicts there will be a Dengue Fever outbreak within 2 months"}
        self.assertEqual(response_json, expected_json)

    def test_xtreme_predict_file_noncsv_within_checked(self):

        with open('TestFile.xlsx', 'rb') as f:
            form = {
                'within': 'on',
                'timeframe': 2,
                'file': f
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_xtreme_predict_file_null_within_checked(self):

        with open('TestFile.csv', 'rb') as f:
            form = {
                'within': 'on',
                'timeframe': 2,
                'file': (f, '')
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_xtreme_predict_timeframe_null_within_checked(self):

        with open('TestFile.csv', 'rb') as f:
            form = {
                'within': 'on',
                'timeframe': "",
                'file': f
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)


    def test_xtreme_predict_all_valid_within_unchecked(self):

        with open('TestFile.csv', 'rb') as f:
            form = {
                'within': '',
                'timeframe': 2,
                'file': f
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": False,"msg": "The Ensemble model predicts there will be a Dengue Fever outbreak in 2 months"}
        self.assertEqual(response_json, expected_json)

    def test_xtreme_predict_file_noncsv_within_unchecked(self):

        with open('TestFile.xlsx', 'rb') as f:
            form = {
                'within': '',
                'timeframe': 2,
                'file': f
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_xtreme_predict_file_null_within_unchecked(self):

        with open('TestFile.csv', 'rb') as f:
            form = {
                'within': '',
                'timeframe': 2,
                'file': (f, '')
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_xtreme_predict_timeframe_null_within_unchecked(self):

        with open('TestFile.csv', 'rb') as f:
            form = {
                'within': '',
                'timeframe': "",
                'file': f
            }
            response = self.client.post('/predictXtreme', data=form)

        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_disease_plot_all_valid(self):
        form = {
            'province': 'An Giang',
            'start': '2012-01',
            'end': '2012-12',
            'disease': 'Dengue_fever_cases',
            'sd': 0
        }
        response = self.client.post('/plotdisease', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json['Error'], False)

    def test_disease_plot_province_null(self):
        form = {
            'province': ' ',
            'start': '2012-01',
            'end': '2012-12',
            'disease': 'Dengue_fever_cases',
            'sd': 0
        }
        response = self.client.post('/plotdisease', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_disease_plot_start_null(self):
        form = {
            'province': 'An Giang',
            'start': '',
            'end': '2012-12',
            'disease': 'Dengue_fever_cases',
            'sd': 0
        }
        response = self.client.post('/plotdisease', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_disease_plot_end_null(self):
        form = {
            'province': 'An Giang',
            'start': '2012-01',
            'end': '',
            'disease': 'Dengue_fever_cases',
            'sd': 0
        }
        response = self.client.post('/plotdisease', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_disease_plot_disease_null(self):
        form = {
            'province': 'An Giang',
            'start': '2012-01',
            'end': '2012-12',
            'disease': '',
            'sd': 0
        }
        response = self.client.post('/plotdisease', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_disease_plot_sd_negative(self):
        form = {
            'province': ' ',
            'start': '2012-01',
            'end': '2012-12',
            'disease': 'Dengue_fever_cases',
            'sd': -1
        }
        response = self.client.post('/plotdisease', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_disease_plot_end_preceeds_start(self):
        form = {
            'province': 'An Giang',
            'start': '2012-12',
            'end': '2012-01',
            'disease': 'Dengue_fever_cases',
            'sd': 0
        }
        response = self.client.post('/plotdisease', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Ensure Start Date preceeds End Date"}
        self.assertEqual(response_json, expected_json)
        

    def test_climate_plot_all_valid(self):
        form = {
            'province': 'An Giang',
            'start': '2012-01',
            'end': '2012-12',
            'env_factor': ['n_raining_days', 'Total_Rainfall'],
            'sd': 0
        }
        response = self.client.post('/plotfactor', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json['Error'], False)

    def test_climate_plot_province_null(self):
        form = {
            'province': ' ',
            'start': '2012-01',
            'end': '2012-12',
            'env_factor': ['n_raining_days', 'Total_Rainfall'],
            'sd': 0
        }
        response = self.client.post('/plotfactor', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_climate_plot_start_null(self):
        form = {
            'province': 'An Giang',
            'start': '',
            'end': '2012-12',
            'env_factor': ['n_raining_days', 'Total_Rainfall'],
            'sd': 0
        }
        response = self.client.post('/plotfactor', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_climate_plot_end_null(self):
        form = {
            'province': 'An Giang',
            'start': '2012-01',
            'end': '',
            'env_factor': ['n_raining_days', 'Total_Rainfall'],
            'sd': 0
        }
        response = self.client.post('/plotfactor', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_climate_plot_disease_null(self):
        form = {
            'province': 'An Giang',
            'start': '2012-01',
            'end': '2012-12',
            'env_factor': [],
            'sd': 0
        }
        response = self.client.post('/plotfactor', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_climate_plot_sd_negative(self):
        form = {
            'province': ' ',
            'start': '2012-01',
            'end': '2012-12',
            'env_factor': ['n_raining_days', 'Total_Rainfall'],
            'sd': -1
        }
        response = self.client.post('/plotfactor', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Please Input all required fields"}
        self.assertEqual(response_json, expected_json)

    def test_climate_plot_end_preceeds_start(self):
        form = {
            'province': 'An Giang',
            'start': '2012-12',
            'end': '2012-01',
            'env_factor': ['n_raining_days', 'Total_Rainfall'],
            'sd': 0
        }
        response = self.client.post('/plotfactor', data=form)
        self.assertEqual(response.status_code, 200)
        response_json = response.json
        expected_json = {"Error": True,"msg": "Ensure Start Date preceeds End Date"}
        self.assertEqual(response_json, expected_json)


if __name__ == "__main__":
    unittest.main()