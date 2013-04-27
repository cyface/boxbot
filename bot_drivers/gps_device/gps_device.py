"""
This class is a facade for calling a GPS device.
The goal is to provide a unified API for various back-ends, and to enable calling a 'fake' GPS for test/dev
"""

import datetime

class GPSDevice():
    """Base Class Representing a GPS Device"""

    latitude = 40.00000
    longitude = -105.0000
    velocity = 15
    altitude = 5280.0
    heading = 180
    time = datetime.time(0,0,0)
    date = datetime.date(1901,1,1)
    date_time = datetime.datetime(1901,1,1,0,0,0)
    ready = False

    def get_current_point(self):
        """Returns a tuple of the current latitude, longitude in decimal format"""
        return self.get_current_latitude(), self.get_current_longitude()

    def get_current_latitude(self):
        """Returns current latitude in decimal format"""
        return self.latitude

    def get_current_longitude(self):
        """Returns the current longitude in decimal format"""
        return self.longitude

    def get_current_speed(self):
        """Returns the current GPS-derived speed in miles per hour"""
        return self.velocity

    def get_current_altitude(self):
        """Returns the current altitude in decimal feet"""
        return self.altitude

    def get_current_altitude_meters(self):
        """Returns the current altitude in decimal meters"""
        return self.altitude * 1609.344

    def get_current_velocity_meters(self):
        """Returns the current GPS-derived speed in meters per second"""
        return self.velocity * 0.44704

    def get_current_velocity_kilometers(self):
        """Returns the current GPS-derived speed in kilometers per hour"""
        return self.velocity * 1.609344

    def get_current_heading(self):
        """Returns the current GPS-derived heading in degrees"""
        return self.heading

    def get_current_heading_radians(self):
        """Returns the current GPS-derived heading in radians"""
        return self.heading * 0.0174532925

    def get_time(self):
        """Returns a datetime.time object with the current time from the GPS"""
        return self.time

    def get_date(self):
        """Returns a datetime.date object with the current date from the GPS"""
        return self.date

    def get_datetime(self):
        """Returns a datetime.datetime object with the current date and time from the GPS"""
        return self.date_time

    def is_ready(self):
        """Returns True if the GPS is ready to return data (on, booted, sat lock, etc.)"""
        return self.ready

    def activate(self):
        """Tells the GPS to do what it needs to do to get ready to return data, sets is_ready() to True when done"""
        self.ready = True

    def deactivate(self):
        """Tells the GPS to shut down, sets is_ready() to False when done"""
        self.ready = False