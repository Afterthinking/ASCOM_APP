from skyfield.api import Topos, Loader
from skyfield.sgp4lib import EarthSatellite

# TLE data
line1 = "1 48274U 21035A   23124.00000000  .00030870  00000-0  46103-3 0  9993"
line2 = "2 48274  41.4742  64.7517 0006054 189.2282  92.0876 15.62688689114935"

# Create an EarthSatellite object

satellite = EarthSatellite(line1, line2)

# Set up the timescale
load = Loader("skyfield_data")
ts = load.timescale()
t = ts.now()

# Create a Topos object representing the observer's location
# Replace these values with the observer's actual latitude, longitude, and elevation
observer_lat = 40.7128
observer_lon = -74.0060
observer_elevation = 0.0
observer = Topos(observer_lat, observer_lon, elevation_m=observer_elevation)

# Compute the position of the satellite relative to the observer
difference = satellite - observer
topocentric = difference.at(t)

# Get latitude, longitude, and elevation
alt, az, _ = topocentric.altaz()

print(f"ISS position at {t.utc_datetime()} UTC relative to the observer:")
print(f"Altitude: {alt.degrees}°")
print(f"Azimuth: {az.degrees}°")