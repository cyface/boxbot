"""
    Tests for the GPSReplay Implementation of the GPSDevice Specification
"""

import unittest
from drivers.gps.gps_replay import GPSReplay


class GPSReplayTests(unittest.TestCase):
    def setUp(self):
        self.gps_replay = GPSReplay()
        self.gps_replay.set_replay_file_path('gps_replay_test_file.csv')
        self.gps_replay.activate()

    def tearDown(self):
        self.gps_replay.deactivate()

    def test_load_file(self):
        """Tests loading a replay file into the object"""
        # Setting of file name happens up in setUp, this is testing that it works
        self.assertEquals('gps_replay_test_file.csv', self.gps_replay.get_replay_file_path())

    def test_get_replay(self):
        """Tests that getting from the replay is working"""
        self.assertEquals('Date,Time,Lat,Long,Altitude,Velocity,Heading\n', self.gps_replay._get_current_replay())
        self.assertEquals('8/13/12,0:16:52,39.72042167,-104.706285,5280,0,0\n', self.gps_replay._get_current_replay())

    def test_get_point(self):
        """Tests getting the current lat/long point"""
        self.gps_replay._advance()
        self.assertEquals((39.72042167, -104.706285), self.gps_replay.get_current_point())
        self.gps_replay._advance()
        self.assertEquals((39.720425, -104.7062867), self.gps_replay.get_current_point())


