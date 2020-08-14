import unittest
from unittest.mock import patch
import os
from app.application import create_app


class ApplicationTest(unittest.TestCase):
    # Note: setUp and tearDown follow a non-standard naming convention
    # because they are based on JUnit which doesn't conform to PEP-0008
    def setUp(self):
        # Create a dummy database for the test case
        self.maxDiff = None

        # Create a dummy db
        db_name = "test.db"
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
        with open(self.db_path, 'w') as f:
            pass

        # Create the app
        # We have to patch the environment to use our dummy database
        with patch('app.application.os') as mocked_os:
            mocked_os.environ.get.return_value = f"sqlite:///{self.db_path}"
            app = create_app()

        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        # Remove the dummy database after the test case
        os.system(f"rm -f {self.db_path}")

    def test_get_regions(self):
        # Basic test with no data
        response = self.app.get("/api/regions")
        self.assertTrue(response.status_code == 200)
        regions = response.get_json()
        self.assertTrue(len(regions) == 0)
