"""
    Maps the base GPS class to the Phidgets GPS
"""

from .. import GPSDevice
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.GPS import GPS
import datetime


class GPSPhidgets(GPSDevice):
    """
    This class implements the GPS facade for the Phidgets GPS.
    """

    phidget = None  # Holds reference to Phidget device, populated from activate

    def get_current_latitude(self):
        try:
            self.latitude = self.phidget.getLatitude()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.latitude

    def get_current_longitude(self):
        try:
            self.longitude = self.phidget.getLongitude()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.longitude

    def get_current_velocity(self):
        """Returns the current GPS-derived speed in miles per hour"""
        try:
            self.velocity = self.phidget.getVelocity()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.velocity

    def get_current_altitude(self):
        """Returns the current altitude in decimal feet"""
        try:
            self.altitude = self.phidget.getAltitude()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.altitude

    def get_current_heading(self):
        """Returns the current GPS-derived heading in degrees"""
        try:
            self.heading = self.phidget.getHeading()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.heading

    def get_time(self):
        """Returns a datetime.time object with the current time from the GPS"""
        try:
            phidget_time = self.phidget.getTime()
            self.time = datetime.time(phidget_time.tm_hour, phidget_time.tm_min, phidget_time.tm_sec, phidget_time.tm_ms)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.time

    def get_date(self):
        """Returns a datetime.date object with the current date from the GPS"""
        try:
            phidget_date = self.phidget.getDate()
            self.date = datetime.date(phidget_date.tm_year, phidget_date.tm_mon, phidget_date.tm_mday)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.date

    def get_datetime(self):
        """Returns a datetime.datetime object with the current date and time from the GPS"""
        try:
            self.date_time = datetime.datetime.combine(self.get_date(), self.get_time())
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
        return self.date_time

    def is_ready(self):
        """Returns True if the GPS is ready to return data (on, booted, sat lock, etc.)"""
        fix_status = self.phidget.getPositionFixStatus()
        if not fix_status:
            self.ready = False
        return self.ready

    def activate(self):
        """Phidget GPS Must be attached via USB cable and powered before calling, sets is_ready() to True when done"""

        try:
            self.phidget = GPS()
            self.phidget.openPhidget()
        except RuntimeError as e:
            print("Runtime Exception: %s" % e.details)

        try:
            self.phidget.waitForAttach(10000)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            try:
                self.phidget.closePhidget()
            except PhidgetException as e:
                print("Phidget Exception %i: %s" % (e.code, e.details))

        self.ready = True

    def deactivate(self):
        """Tells the GPS to shut down, sets is_ready() to False when done"""
        self.phidget.closePhidget()
        self.ready = False
