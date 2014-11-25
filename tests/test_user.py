from test_base import BaseTestCase

from flask import session


class UserTestCase(BaseTestCase):

    # HELPER METHODS
    def login(self, email, password):
        return self.client.post('user/login',
                                data=dict(email=email,
                                          password=password),
                                follow_redirects=True
                                )

    def logout(self):
        return self.client.get('user/logout', follow_redirects=True)

    # TESTS
    def test_correct_login(self):
        with self.client:
            resp = self.login('admin@email.com', 'admin')
            self.assertIn(b'You have successfully logged in!', resp.data)
            self.assertTrue(session['user_name'] == 'admin')
            self.assertTrue(session['user_id'] == 1)

    def test_logout(self):
        with self.client:
            self.login('admin@email.com', 'admin')
            resp = self.logout()
            self.assertTrue(b'You have logged out!' in resp.data)

    def test_login_failed(self):
        with self.client:
            resp = self.login('joe@example.com', 'blow')
            self.assertIn(b'Username or Password is incorrect!', resp.data)

    def test_404(self):
        with self.client:
            resp = self.client.get('some-page-that-doesnt-exist',
                                   follow_redirects=True)
            self.assertIn(b'404', resp.data)
            self.assertEqual(resp.status_code, 404)

    def test_create_user_success(self):
        with self.client:
            self.login('admin@email.com', 'admin')
            resp = self.client.post('user/create',
                                    data=dict(name='test user',
                                              email='test@email.com',
                                              password='password',
                                              password_confirm='password',
                                              role='user'),
                                    follow_redirects=True,
                                    )
            self.assertIn(b'User created!', resp.data)

    def test_login_required(self):
        with self.client:
            resp = self.client.get('user/create', follow_redirects=True)
            self.assertIn(b'Login Required!', resp.data)

    def test_access_denied_for_basic_user(self):
            self.login('admin@email.com', 'admin')
            self.client.post('user/create',
                             data=dict(name='test user',
                                       email='test@email.com',
                                       password='password',
                                       password_confirm='password',
                                       role='user'),
                             follow_redirects=True,
                             )
            self.logout()
            self.login('test@email.com', 'password')
            resp = self.client.get('user/create', follow_redirects=True)
            self.assertIn(b'ACCESS DENIED!', resp.data)
