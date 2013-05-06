import ConfigParser

### Write
config = ConfigParser.ConfigParser()

config.add_section('ports')
config.set('ports', 'compass', '/dev/ttyUSB0')
config.set('ports', 'gps', '/dev/ttyACM0')
config.set('ports', 'servos', '/dev/ttyACM2')

with open('bot.cfg', 'wb') as configfile:
    config.write(configfile)

### Read
config = ConfigParser.ConfigParser()
config.read('bot.cfg')

print config.get('ports', 'compass')
print config.get('ports', 'gps')
print config.get('ports', 'servos')

### Waypoints

config = ConfigParser.ConfigParser()

### Write Waypoints
config.add_section('1')
config.set('1', 'latitude', 39.101233)
config.set('1', 'longitude', -104.01234)

with open('waypoints.cfg', 'wb') as configfile:
    config.write(configfile)

config = ConfigParser.ConfigParser()
config.read('waypoints.cfg')
waypoints = config.sections()
for waypoint in waypoints:
    print 'Lat: ' + config.get(waypoint, 'latitude')
    print 'Lng: ' + config.get(waypoint, 'longitude')