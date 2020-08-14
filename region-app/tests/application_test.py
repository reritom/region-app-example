import unittest
from unittest.mock import patch
import os
from app.application import create_app, seed


class ApplicationTest(unittest.TestCase):
    # Note: setUp and tearDown follow a non-standard naming convention
    # because they are based on JUnit which doesn't conform to PEP-0008
    def setUp(self):
        # Create a dummy database for the test case
        self.maxDiff = None

        # Create a dummy db
        db_name = "test.db"
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.dir_path, db_name)
        with open(self.db_path, 'w') as f:
            pass

        # Create the app
        # We have to patch the environment to use our dummy database
        with patch('app.application.os') as mocked_os:
            mocked_os.environ.get.return_value = f"sqlite:///{self.db_path}"
            app = create_app()

        app.testing = True
        self.uninstanciated_app = app
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

    def test_populate_and_get_regions(self):
        # Test the population works
        runner = self.uninstanciated_app.test_cli_runner()

        # Invoke the command directly
        result = runner.invoke(seed, [os.path.join(os.path.dirname(self.dir_path), "static", "correspondance-code-insee-code-postal.csv")])
        # If there is something failing in the seed function, this below print statement is pretty much the only place to see it.
        # print(result) # Keep this for future debugging

        # Patch our controller so avoid using the api. Our unit test should not be coupled to an external provider
        with patch("app.controllers.region_controller.OSMApi") as dummy_osm:
            dummy_osm.get_state_details.return_value = None
            response = self.app.get("/api/regions")

        self.assertTrue(response.status_code == 200)

        # Check the regions are visible, there should be 27
        regions = response.get_json()
        self.assertEqual(len(regions), 27)
