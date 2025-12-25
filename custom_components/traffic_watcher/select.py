from homeassistant.components.select import SelectEntity

from .const import DATA_LAUNCH_MAPS, DATA_LAUNCH_MAPS_NEVER, DATA_LAUNCH_MAPS_WHEN_BEST_ROUTE_DIFFERENT, \
    DATA_LAUNCH_MAPS_ALWAYS
from .const import DOMAIN
from .entity import TrafficWatcherEntity


async def async_setup_entry(hass, entry, async_add_devices):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([
        LaunchMapsSelect(coordinator, entry),
    ])


class LaunchMapsSelect(TrafficWatcherEntity, SelectEntity):
    def select_option(self, option: str):
        self.coordinator.data[DATA_LAUNCH_MAPS] = option

    @property
    def name(self):
        return f"{self.person_name} Launch Map On Commute"

    @property
    def icon(self):
        return "mdi:map"

    @property
    def options(self):
        return [
            DATA_LAUNCH_MAPS_NEVER,
            DATA_LAUNCH_MAPS_WHEN_BEST_ROUTE_DIFFERENT,
            DATA_LAUNCH_MAPS_ALWAYS
        ]

    @property
    def current_option(self):
        return self.coordinator.data[DATA_LAUNCH_MAPS]
