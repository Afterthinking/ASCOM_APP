from skyfield.api import Topos, load

ts = load.timescale()
t = ts.now()

planets = load('de421.bsp')
earth = planets['earth']

# Topos represents a position on the Earth. Fill in your latitude and longitude here.
my_location = earth + Topos('23.0578 N', '115.0564 W')

# Get the position of Polaris
polaris = my_location.at(t).from_altaz(alt_degrees=90.0, az_degrees=0.0)

# The position is returned as a tuple of 3 values: (RA, DEC, distance).
# The distance is not used for a star like Polaris, because all stars are effectively at infinite distance.
ra, dec, _ = polaris.radec()

print('RA:', ra.hours)
print('DEC:', dec.degrees)