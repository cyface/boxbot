from csv import DictReader
import os
from upoints import point

brain_dir = PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

waypoint_file = file(os.path.join(brain_dir, "", "school_points.csv"))
waypoints = []
for waypoint in DictReader(waypoint_file):
    waypoints.append(waypoint)
print waypoints
curr_waypoint = 0
curr_waypoint_point = point.Point(waypoints[curr_waypoint].get('Latitude'), waypoints[curr_waypoint].get('Longitude'))

print curr_waypoint_point