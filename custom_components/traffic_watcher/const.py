"""Constants for Traffic Watcher."""
# Base component constants
NAME = "Traffic Watcher"
DOMAIN = "traffic_watcher"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/jpitlor/traffic-watcher/issues"

# Platforms
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [SENSOR, SWITCH]

# Configuration and options
CONF_PERSON = "person"
CONF_PHONE = "phone"
CONF_HOME = "home"
CONF_WORK = "work"
CONF_SCHEDULE = "schedule"
CONF_API_KEY = "api_key"
CONF_SERVICE_ACCOUNT_JSON = "service_account_json"

# Data
DATA_USUAL_ROUTE = "usual_route"
DATA_CURRENT_ROUTE = "current_route"
DATA_USUAL_ROUTE_TIME = "usual_route_time"
DATA_CURRENT_ROUTE_TIME = "current_route_time"
DATA_MONTHLY_API_CALLS = "monthly_api_calls"
DATA_LAUNCH_MAPS = "launch_maps"

# Select Options
DATA_LAUNCH_MAPS_ALWAYS = "Always"
DATA_LAUNCH_MAPS_WHEN_BEST_ROUTE_DIFFERENT = "When best route is different"
DATA_LAUNCH_MAPS_NEVER = "Never"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
