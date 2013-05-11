import os
import ConfigParser
from upoints import point

test_dir = os.path.abspath(os.path.dirname(__file__))

waypoint_file_path = os.path.join(test_dir, "../brains/waypoints/school_points.cfg")
waypoint_config = ConfigParser.RawConfigParser()
waypoint_config.read(waypoint_file_path)
waypoints = []
print waypoint_config.sections()
for waypoint in waypoint_config.sections():
    waypoints.append(point.Point(waypoint_config.get(waypoint, 'latitude'), waypoint_config.get(waypoint, 'longitude')))
curr_waypoint = 0

print waypoints