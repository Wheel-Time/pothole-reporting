from decimal import Decimal
from django.test import TestCase, Client
from django.db import connection
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time
from pothole_reporting.models import Pothole, SiteUser, PotholeLedger, VwPothole

def setUpDB():
    with open('../sql/test-pothole-database.sql', 'r') as content_file:
        pothole_db = content_file.read()
    with open('../sql/test-views.sql', 'r') as content_file:
        pothole_vw = content_file.read()
    connection.cursor().execute(pothole_db)
    connection.cursor().execute(pothole_vw)
    SiteUser.objects.create(
        username='SYSTEM',
        first_name='wheel',
        last_name='time',
        email='WheelTimePotholes@gmail.com',
        pword='1234',
        is_admin=1)

def tearDownDB():
    connection.cursor().execute("DROP TABLE pothole_ledger")
    connection.cursor().execute("DROP TABLE site_user")
    connection.cursor().execute("DROP TABLE pothole")
    connection.cursor().execute("DROP view vw_pothole")
    connection.cursor().execute("DROP TABLE django_session")
    connection.cursor().execute("DROP TABLE django_migrations")
    connection.cursor().execute("DROP TABLE django_admin_log")
    connection.cursor().execute("DROP TABLE auth_user_user_permissions")
    connection.cursor().execute("DROP TABLE auth_user_groups")
    connection.cursor().execute("DROP TABLE auth_user")
    connection.cursor().execute("DROP TABLE auth_group_permissions")
    connection.cursor().execute("DROP TABLE auth_permission")
    connection.cursor().execute("DROP TABLE django_content_type")
    connection.cursor().execute("DROP TABLE auth_group")

class SubmitTest(TestCase):
    def setUp(self):
        setUpDB()

    def tearDown(self):
        tearDownDB()

    def test_submit_pothole(self):
        c = Client()

        self.assertEqual(0, Pothole.objects.all().count())
        self.assertEqual(0, VwPothole.objects.all().count())
        self.assertEqual(0, PotholeLedger.objects.all().count())

        c.post('/login/', {'username': 'SYSTEM', 'password': '1234'})
        c.post('/submit/', {'lat': 0, 'lon': 0, 'state': 5})

        self.assertEqual(1, VwPothole.objects.all().count())
        self.assertEqual(1, Pothole.objects.all().count())
        self.assertEqual(1, PotholeLedger.objects.all().count())

class UpdateTest(TestCase):
    def setUp(self):
        setUpDB()

    def tearDown(self):
        tearDownDB()

    def test_update_pothole(self):
        c = Client()

        self.assertEqual(0, Pothole.objects.all().count())
        self.assertEqual(0, VwPothole.objects.all().count())
        self.assertEqual(0, PotholeLedger.objects.all().count())

        c.post('/login/', {'username': 'SYSTEM', 'password': '1234'})
        c.post('/submit/', {'lat': 0, 'lon': 0, 'state': 5})

        self.assertEqual(1, VwPothole.objects.all().count())
        self.assertEqual(1, Pothole.objects.all().count())
        self.assertEqual(1, PotholeLedger.objects.all().count())

        c.post('/update/', {'pothole_id': 1, 'state': 5})

        self.assertEqual(1, VwPothole.objects.all().count())
        self.assertEqual(1, Pothole.objects.all().count())
        self.assertEqual(2, PotholeLedger.objects.all().count())

class ConfirmTest(TestCase):
    def setUp(self):
        setUpDB()

    def tearDown(self):
        tearDownDB()

    def test_update_pothole(self):
        c = Client()

        self.assertEqual(0, Pothole.objects.all().count())
        self.assertEqual(0, VwPothole.objects.all().count())
        self.assertEqual(0, PotholeLedger.objects.all().count())

        c.post('/login/', {'username': 'SYSTEM', 'password': '1234'})
        c.post('/submit/', {'lat': 0, 'lon': 0, 'state': 5})

        pothole = VwPothole.objects.get(id=1)
        self.assertIsNone(pothole.effective_date)
        self.assertEqual('9999-12-31 23:59:59', pothole.fixed_date)

        c.post('/update/', {'pothole_id': 1, 'state': 5})
        c.post('/update/', {'pothole_id': 1, 'state': 4})
        c.post('/update/', {'pothole_id': 1, 'state': 5})
        c.post('/update/', {'pothole_id': 1, 'state': 3})
        c.post('/update/', {'pothole_id': 1, 'state': 4})
        c.post('/update/', {'pothole_id': 1, 'state': 5})

        pothole = VwPothole.objects.get(id=1)

        self.assertEqual(1, VwPothole.objects.all().count())
        self.assertEqual(1, Pothole.objects.all().count())
        self.assertEqual(7, PotholeLedger.objects.all().count())
        self.assertAlmostEqual(Decimal(31/7), pothole.avg_severity, places=3)
        self.assertIsNotNone(pothole.effective_date)
        self.assertEqual('9999-12-31 23:59:59', pothole.fixed_date)

class MarkFixedTest(TestCase):
    def setUp(self):
        setUpDB()

    def tearDown(self):
        tearDownDB()

    def test_update_pothole(self):
        c = Client()

        self.assertEqual(0, Pothole.objects.all().count())
        self.assertEqual(0, VwPothole.objects.all().count())
        self.assertEqual(0, PotholeLedger.objects.all().count())

        c.post('/login/', {'username': 'SYSTEM', 'password': '1234'})
        c.post('/submit/', {'lat': 0, 'lon': 0, 'state': 5})

        pothole = VwPothole.objects.get(id=1)
        self.assertIsNone(pothole.effective_date)
        self.assertEqual('9999-12-31 23:59:59', pothole.fixed_date)

        c.post('/update/', {'pothole_id': 1, 'state': 5})
        c.post('/update/', {'pothole_id': 1, 'state': 4})
        c.post('/update/', {'pothole_id': 1, 'state': 5})
        c.post('/update/', {'pothole_id': 1, 'state': 3})
        c.post('/update/', {'pothole_id': 1, 'state': 4})
        c.post('/update/', {'pothole_id': 1, 'state': 5})

        c.post('/update/', {'pothole_id': 1, 'state': 0})
        c.post('/update/', {'pothole_id': 1, 'state': 0})
        c.post('/update/', {'pothole_id': 1, 'state': 0})
        c.post('/update/', {'pothole_id': 1, 'state': 0})
        c.post('/update/', {'pothole_id': 1, 'state': 0})
        c.post('/update/', {'pothole_id': 1, 'state': 0})

        pothole = VwPothole.objects.get(id=1)

        self.assertEqual(1, VwPothole.objects.all().count())
        self.assertEqual(1, Pothole.objects.all().count())
        self.assertEqual(13, PotholeLedger.objects.all().count())
        self.assertIsNotNone(pothole.effective_date)
        self.assertNotEqual('9999-12-31 23:59:59', pothole.fixed_date)

class SignupTest(TestCase):
    def setUp(self):
        setUpDB()

    def tearDown(self):
        tearDownDB()

    def test_submit_pothole(self):
        c = Client()

        self.assertEqual(1, SiteUser.objects.all().count())

        c.post('/signup/', {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test_user@test.email',
            'password1': 'test_pass',
            'password2': 'test_pass'
        })

        self.assertEqual(2, SiteUser.objects.all().count())

class SeleniumLoginTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setUpDB()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        tearDownDB()
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('SYSTEM')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1234')
        self.selenium.find_element_by_name("login").click()
        self.assertEqual("Home | Pothole Reporting", self.selenium.title)

class SeleniumSignupTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setUpDB()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        tearDownDB()
        cls.selenium.quit()
        super().tearDownClass()

    def test_signup(self):
        username = 'test'
        first_name = 'test'
        last_name = 'user'
        email = 'test_user@test.email'
        password1 = 'test_pass'
        password2 = 'test_pass'

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password1)
        self.selenium.find_element_by_name("login").click()
        self.assertEqual("Login | Pothole Reporting", self.selenium.title)

        self.selenium.get('%s%s' % (self.live_server_url, '/signup/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        first_name_input = self.selenium.find_element_by_name("first_name")
        first_name_input.send_keys(first_name)
        last_name_input = self.selenium.find_element_by_name("last_name")
        last_name_input.send_keys(last_name)
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys(email)
        password1_input = self.selenium.find_element_by_name("password1")
        password1_input.send_keys(password1)
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys(password2)
        self.selenium.find_element_by_name("create").click()
        self.assertEqual("Login | Pothole Reporting", self.selenium.title)

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password1)
        self.selenium.find_element_by_name("login").click()
        self.assertEqual("Home | Pothole Reporting", self.selenium.title)

class SeleniumCreateTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setUpDB()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        tearDownDB()
        cls.selenium.quit()
        super().tearDownClass()

    def test_create(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('SYSTEM')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1234')
        self.selenium.find_element_by_name("login").click()
        self.assertEqual("Home | Pothole Reporting", self.selenium.title)

        self.selenium.get('%s%s' % (self.live_server_url, '/submit/'))
        action = webdriver.common.action_chains.ActionChains(self.selenium)
        action.move_to_element_with_offset(self.selenium.find_element_by_id('map'), 500, 500)
        action.click()
        action.perform()
        time.sleep(3)
        self.selenium.find_element_by_id('select-4').click()
        self.selenium.find_element_by_id('submit-button').click()
        alert = self.selenium.switch_to_alert()
        self.assertEqual("Successfully created a new pothole", alert.text)
        alert.accept()

class SeleniumConfirmTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setUpDB()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        tearDownDB()
        cls.selenium.quit()
        super().tearDownClass()

    def test_confirm(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('SYSTEM')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1234')
        self.selenium.find_element_by_name("login").click()
        self.assertEqual("Home | Pothole Reporting", self.selenium.title)

        self.selenium.get('%s%s' % (self.live_server_url, '/submit/'))
        action = webdriver.common.action_chains.ActionChains(self.selenium)
        action.move_to_element_with_offset(self.selenium.find_element_by_id('map'), 600, 450)
        action.click()
        action.perform()
        time.sleep(3)
        self.selenium.find_element_by_id('select-4').click()
        self.selenium.find_element_by_id('submit-button').click()
        alert = self.selenium.switch_to_alert()
        self.assertEqual("Successfully created a new pothole", alert.text)
        alert.accept()
        self.selenium.switch_to_default_content()
        action = webdriver.common.action_chains.ActionChains(self.selenium)
        action.move_to_element_with_offset(self.selenium.find_element_by_id('map'), 600, 450)
        action.move_by_offset(10, 10)
        action.move_by_offset(-10, -10)
        action.perform()
        time.sleep(1)
        self.selenium.find_element_by_id('confirm-button').click()
        time.sleep(3)
        self.selenium.find_element_by_id('select-4').click()
        self.selenium.find_element_by_id('submit-button').click()
        alert = self.selenium.switch_to_alert()
        self.assertEqual("Successfully submitted pothole report", alert.text)
        alert.accept()

class SeleniumFixTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setUpDB()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        tearDownDB()
        cls.selenium.quit()
        super().tearDownClass()

    def test_fix(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('SYSTEM')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1234')
        self.selenium.find_element_by_name("login").click()
        self.assertEqual("Home | Pothole Reporting", self.selenium.title)

        self.selenium.get('%s%s' % (self.live_server_url, '/submit/'))
        action = webdriver.common.action_chains.ActionChains(self.selenium)
        action.move_to_element_with_offset(self.selenium.find_element_by_id('map'), 600, 450)
        action.click()
        action.perform()
        time.sleep(3)
        self.selenium.find_element_by_id('select-4').click()
        self.selenium.find_element_by_id('submit-button').click()
        alert = self.selenium.switch_to_alert()
        self.assertEqual("Successfully created a new pothole", alert.text)
        alert.accept()
        self.selenium.switch_to_default_content()
        action = webdriver.common.action_chains.ActionChains(self.selenium)
        action.move_to_element_with_offset(self.selenium.find_element_by_id('map'), 600, 450)
        action.move_by_offset(10, 10)
        action.move_by_offset(-10, -10)
        action.perform()
        self.selenium.find_element_by_id('fixed-button').click()
        alert = self.selenium.switch_to_alert()
        self.assertEqual("Successfully submitted pothole report", alert.text)
        alert.accept()

