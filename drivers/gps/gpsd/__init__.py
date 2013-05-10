"""
    Maps the base GPS class to a Linux gpsd GPS
"""

from .. import GPSDevice
from gps import *


class GPSDGPS(GPSDevice):
    """
    This class implements the GPS Driver for the GPSD GPS.
    """

    gpsd = None  # Holds reference to gpsd device, populated from activate

    def get_current_latitude(self):
        return self.latitude

    def get_current_longitude(self):
        return self.longitude

    def get_current_velocity(self):
        """Returns the current GPS-derived speed in miles per hour"""
        return self.velocity

    def get_current_altitude(self):
        """Returns the current altitude in decimal feet"""
        return self.altitude

    def get_current_heading(self):
        """Returns the current GPS-derived heading in degrees"""
        return self.heading

    def get_time(self):
        """Returns a datetime.time object with the current time from the GPS"""
        return self.date_time

    def get_date(self):
        """Returns a datetime.date object with the current date from the GPS"""
        return self.date_time

    def get_datetime(self):
        """Returns a datetime.datetime object with the current date and time from the GPS"""
        return self.date_time

    def is_ready(self):
        """Returns True if the GPS is ready to return data (on, booted, sat lock, etc.)"""
        return True

    def activate(self):
        """GPS must be attached and GPSD must be running before calling"""

        self.gpsd = gps(mode=WATCH_ENABLE)
        self.ready = True

    def update(self):
        gps_data = self.gpsd.next()
        self.date_time = gps_data.get('time', "")
        self.latitude = gps_data.get('lat', 0.0)
        self.longitude = gps_data.get('lon', 0.0)
        self.heading = gps_data.get('track', 0.0)

    def deactivate(self):
        """Tells the GPS to shut down, sets is_ready() to False when done"""
        self.ready = False

__author__ = 'cyface'
