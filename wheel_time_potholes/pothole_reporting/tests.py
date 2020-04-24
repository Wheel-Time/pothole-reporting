from decimal import Decimal
from django.test import TestCase, Client
from django.db import connection
from django.utils import timezone
from pothole_reporting.models import Pothole, SiteUser, PotholeLedger, VwPothole

# Create your tests here.
def setUpDB():
    with open('../sql/pothole-database.sql', 'r') as content_file:
        pothole_db = content_file.read()
    with open('../sql/views.sql', 'r') as content_file:
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

        respose = c.post('/signup/', {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test_user@test.email',
            'password1': 'test_pass',
            'password2': 'test_pass'
        })

        self.assertEqual(2, SiteUser.objects.all().count())

