"""Switch platform for Traffic Watcher."""
from homeassistant.components.switch import SwitchEntity

from .const import DATA_LAUNCH_MAPS, CONF_PERSON
from .const import DOMAIN
from .entity import TrafficWatcherEntity


async def async_setup_entry(hass, entry, async_add_devices):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([
        LaunchMapsBinarySwitch(coordinator, entry),
    ])


class LaunchMapsBinarySwitch(TrafficWatcherEntity, SwitchEntity):
    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        self.coordinator.data[DATA_LAUNCH_MAPS] = True

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        self.coordinator.data[DATA_LAUNCH_MAPS] = False

    @property
    def name(self):
        return f"{self.person_name} Launch Map On Commute"

    @property
    def icon(self):
        return "mdi:map"

    @property
    def is_on(self):
        return self.coordinator.data.get(DATA_LAUNCH_MAPS)
