from django.test import TestCase
from django.urls import reverse

# Checks that the "index" view uses the right template and returns the status code 200
class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

# Checks that the "song" view uses the right template and returns the status code 200
class SongViewTest(TestCase):
    def test_songs_view(self):
        response = self.client.get(reverse('songs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'songs.html')

# Checks that the "photos" view uses the right template and returns the status code 200
class PhotosViewTest(TestCase):
    def test_photos_view(self):
        response = self.client.get(reverse('photos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos.html')

# Checks that the "login" view uses the right template and returns the status code 200
class LoginViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

# Checks that the "logout" view uses the right template and returns the status code 200
class LogoutViewTest(TestCase):
    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

# Checks that the "signup" view uses the right template and returns the status code 200
class SignupViewTest(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

# Checks that the "concerts" view uses the right template and returns the status code 200
class ConcertsViewTest(TestCase):
    def test_concerts_view(self):
        response = self.client.get(reverse('concerts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'concerts.html')

