import unittest
from app import app, food_entries

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        food_entries.clear()

    def test_BMRCalc_get(self):
        result = self.app.get('/second')
        self.assertEqual(result.status_code, 200)
        print(result.data.decode())
        self.assertIn(b'BMR Calculator', result.data)

    def test_BMRCalc_post(self):
        result = self.app.post('/second', data=dict(weight="150", height="65", age="30", sex="M"))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Your BMR is', result.data)

    def test_BMRCalc_invalid_post(self):
        result = self.app.post('/second', data=dict(weight="invalid", height="invalid", age="invalid", sex="M"))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Please enter valid numeric values for weight, height, and age.', result.data)

    def test_BMICalc_get(self):
        result = self.app.get('/third')
        self.assertEqual(result.status_code, 200)
        print(result.data.decode())
        self.assertIn(b'BMI Calculator', result.data)

    def test_BMICalc_post(self):
        result = self.app.post('/third', data=dict(heightFeet="5", heightInches="10", weight="150"))
        self.assertEqual(result.status_code, 200)
        print(result.data.decode())  # Add this line to see the response content
        self.assertIn(b'Your BMI is:', result.data)

    def test_BMICalc_invalid_post(self):
        result = self.app.post('/third', data=dict(heightFeet="invalid", heightInches="invalid", weight="invalid"))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Please enter valid numeric values for weight and height.', result.data)

    def test_food_diary_get(self):
        result = self.app.get('/fourth')
        self.assertEqual(result.status_code, 200)
        print(result.data.decode())
        self.assertIn(b'Food Diary', result.data)

    def test_food_diary_post(self):
        result = self.app.post('/fourth', data=dict(food="Apple", calories="95"))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Apple', result.data)
        self.assertIn(b'95', result.data)

    def test_food_diary_invalid_post(self):
        result = self.app.post('/fourth', data=dict(food="Apple", calories="invalid"))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Please enter a valid number for calories.', result.data)

if __name__ == "__main__":
    unittest.main()
