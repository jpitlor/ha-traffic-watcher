from homeassistant.util import slugify

from .const import DEFAULT_NAME, DATA_CURRENT_ROUTE, DATA_USUAL_ROUTE, DATA_USUAL_ROUTE_TIME, DATA_CURRENT_ROUTE_TIME, \
    DATA_MONTHLY_API_CALLS, CONF_PERSON
from .const import DOMAIN
from .const import SENSOR
from .entity import TrafficWatcherEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([
        UsualRouteSensor(coordinator, entry),
        CurrentRouteSensor(coordinator, entry),
        UsualRouteTimeSensor(coordinator, entry),
        CurrentRouteTimeSensor(coordinator, entry),
        MonthlyApiCallsSensor(coordinator, entry),
    ])


class UsualRouteSensor(TrafficWatcherEntity):
    @property
    def name(self):
        return f"{self.person_name} Usual Route"

    @property
    def state(self):
        return self.coordinator.data.get(DATA_USUAL_ROUTE)

    @property
    def icon(self):
        return "mdi:routes"

    @property
    def device_class(self):
        return "traffic_watcher__route"


class CurrentRouteSensor(TrafficWatcherEntity):
    @property
    def name(self):
        return f"{self.person_name} Current Route"

    @property
    def state(self):
        return self.coordinator.data.get(DATA_CURRENT_ROUTE)

    @property
    def icon(self):
        return "mdi:routes"

    @property
    def device_class(self):
        return "traffic_watcher__route"


class UsualRouteTimeSensor(TrafficWatcherEntity):
    @property
    def name(self):
        return f"{self.person_name} Usual Route Time"

    @property
    def state(self):
        return self.coordinator.data.get(DATA_USUAL_ROUTE_TIME)

    @property
    def device_class(self):
        return "duration"


class CurrentRouteTimeSensor(TrafficWatcherEntity):
    @property
    def name(self):
        return f"{self.person_name} Current Route Time"

    @property
    def state(self):
        return self.coordinator.data.get(DATA_CURRENT_ROUTE_TIME)

    @property
    def device_class(self):
        return "duration"


class MonthlyApiCallsSensor(TrafficWatcherEntity):
    @property
    def name(self):
        return f"{self.person_name} Monthly API Calls"

    @property
    def state(self):
        return self.coordinator.data.get(DATA_MONTHLY_API_CALLS)

    @property
    def icon(self):
        return "mdi:api"
