# This file contains the blocklist of JWT's. It's for logout purposes
# We probably want to use a database rather than a set for this e.g. when we restart the app, the blocklist will be reset. DB will persist

BLOCKLIST = set()