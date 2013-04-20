compass_data = range(0, 360, 5)
bearing_data = range(360, 0, -5)

headings = []

for i in range(0, 20):
    compass_reading = compass_data.pop()
    current_bearing = bearing_data.pop()
    bearing_diff = compass_reading - current_bearing

    print("CMP:{0} BEAR: {1} DIFF: {0}".format(compass_reading, current_bearing, bearing_diff))