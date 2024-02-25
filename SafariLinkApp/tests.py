from django.test import TestCase, Client
from .models import Member, MpesaTransaction  # Replace with your models
from .views import register_view, login_view, book_vehicle  # Replace with relevant views
from django.contrib.auth.models import User  # Assuming User model is used for authentication

# Test helper functions
def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    return user

def create_member(username, password, phone_number):
    member = Member.objects.create(username=username, password=password, phone_number=phone_number)
    return member


class TestRegistrationView(TestCase):
    def test_valid_registration(self):
        # Arrange
        data = {'username': 'testuser', 'password1': 'strong_password', 'password2': 'strong_password'}

        # Act
        response = self.client.post('/register/', data)

        # Assert
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertEqual(User.objects.count(), 1)  # Check for new user in User model

    def test_invalid_registration(self):
        # Arrange
        data = {'username': 'testuser', 'password1': 'weakpassword', 'password2': 'weakpassword'}

        # Act
        response = self.client.post('/register/', data)

        # Assert
        self.assertEqual(response.status_code, 200)  # Render registration form
        self.assertEqual(User.objects.count(), 0)  # No new user created

    def test_duplicate_username(self):
        # Arrange
        create_user('existinguser', 'existingpassword')  # Create a user
        data = {'username': 'existinguser', 'password1': 'testpassword', 'password2': 'testpassword'}

        # Act
        response = self.client.post('/register/', data)

        # Assert
        self.assertEqual(response.status_code, 200)  # Render registration form
        self.assertIn(b'username taken', response.content)  # Check for error message
        self.assertEqual(User.objects.count(), 1)  # No new user created


class TestLoginView(TestCase):
    def test_successful_login(self):
        # Arrange
        user = create_user('kerichfelix', 'kerichfelix')
        data = {'username': 'kerichfelix', 'password': 'kerichfelix'}

        # Act
        response = self.client.post('/login/', data)

        # Assert
        self.assertEqual(response.status_code, 302)  # Redirect to appropriate page
        self.assertTrue(self.client.login(username='kerichfelix', password='kerichfelix'))  # Verify login

    def test_invalid_credentials(self):
        # Arrange
        # No user created beforehand
        data = {'username': 'testuser', 'password': 'wrongpassword'}

        # Act
        response = self.client.post('/login/', data)

        # Assert
        self.assertEqual(response.status_code, 200)  # Render login form
        self.assertContains(response, 'Invalid username or password')  # Check for error message
        self.assertFalse(self.client.login(username='testuser', password='wrongpassword'))  # Verify incorrect login

# Similar test classes for book_vehicle view and other relevant views
# ...

# Sample test for MpesaTransaction model and callback view
class TestMpesaTransaction(TestCase):
    def test_mpesa_transaction_creation(self):
        # Arrange
        # Simulate Mpesa response data (modify to match your specific data structure)
        response_data = {
            'Body': {
                'stkCallback': {
                    'MerchantRequestID': '123456',
                    'CheckoutRequestID': '789012',
                    'ResultCode': 0,  # Success code
                    'CallbackMetadata': {
                        'Item': [
                            {'Name': 'phone_number', 'Value': '254712345678'},
                            # ...other relevant data items
                        ]
                    }
                }
            }
        }

        # Act
        #
