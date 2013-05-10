"""
    Instantiates GPS Interface but replays points from a file rather than live data.
    Useful for testing and development.
"""

from .. import GPSDevice
import datetime


class GPSReplay(GPSDevice):
    """Base Class Representing a GPS Device"""

    replay_file_path = None  # Path to the comma-delimited GPS Replay File
    replay_file = None  # Python File Handle for the GPS Replay File
    current_replay = None  # Current line from replay file

    def get_current_latitude(self):
        """Returns current latitude in decimal format"""
        return self.latitude

    def get_current_longitude(self):
        """Returns the current longitude in decimal format"""
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
        if self.get_replay_file_path() is not None:
            self.replay_file = open(self.replay_file_path)
            self.ready = True
        else:
            self.ready = False
            print ("No Replay File Path Set, Cannot Activate!")

    def deactivate(self):
        """Tells the GPS to shut down, sets is_ready() to False when done"""
        if self.replay_file:
            self.replay_file.close()
        self.ready = False

    def set_replay_file_path(self, path):
        """Sets the path of the file to use to replay GPS data from, must be called before activate"""
        self.replay_file_path = path

    def get_replay_file_path(self):
        """Returns the path of the file to use to replay GPS data from"""
        return self.replay_file_path

    def _get_current_replay(self):
        """Get a new line from the file"""
        if self.replay_file:
            self.current_replay = self.replay_file.readline()
            return self.current_replay
        else:
            self.ready = False
            print ("No Replay File, Cannot Read!")

    def _advance(self):
        """Parse the next line in the file. If it finds a bad line, it tries to go to the next."""
        self._get_current_replay()
        if self.current_replay:
            parts = self.current_replay.split(',')
            if parts[0] != 'Date':
                try:
                    date_parts = parts[0].split('/')
                    self.date = datetime.datetime.strptime(parts[0], '%m/%d/%y')
                    self.time = datetime.datetime.strptime(parts[1], '%H:%M:%S')
                    self.latitude = float(parts[2])
                    self.longitude = float(parts[3])
                    self.altitude = float(parts[4])
                    self.velocity = float(parts[5])
                    self.heading = float(parts[6])
                except (ValueError, IndexError, TypeError) as e:
                    print("Replay Parsing Error: {0}".format(str(e)))
                    self.date = None
                    self.time = None
                    self.latitude = None
                    self.longitude = None
                    self.altitude = None
                    self.velocity = None
                    self.heading = None
                    self._advance()
            else:
                self._advance()
