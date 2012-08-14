from geopy import distance

CORNER_1 = (39.71888, -104.70283)
CORNER_2 = (39.71889, -104.70216)
CORNER_3 = (39.71919, -104.70218)
CORNER_4 = (39.71922, -104.70283)
print (distance.distance(CORNER_1, CORNER_4).feet)

#20:17:14.804,39.720375,-104.7062367,0.00046761,0.016386793

ex_1 = (39.72037833, -104.70624)
ex_2 = (39.720375, -104.7062367)

print (distance.distance(ex_1, ex_2).feet)