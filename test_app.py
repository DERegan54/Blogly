from unittest import TestCase
from app import app
from models import User, Post


class BloglyTests(TestCase):
    """Integration tests for Blogly app."""
    def setUp(self):
        """To do before each test."""
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_homepage_redirect(self):
        with app.test_client() as client:
            resp = client.get("/users", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Users:</h2>', html)

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Blogly</h1>', html)
    
    def test_show_add_user_form(self):
        with app.test_client() as client:
            resp = client.get('users/add_user')
            html = resp.get_data('as_text=True')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Create a user</h2>', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post('users/add_user', data={'user.first_name:"Sally", user.last_name:"Field", image_url=None'})
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="users/user_details/45>Sally Field</a></li>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post('/users/<int:user_id>/delete')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertFalse('<li><a href="users/user_details/45>Sally Field</a></li>', html)