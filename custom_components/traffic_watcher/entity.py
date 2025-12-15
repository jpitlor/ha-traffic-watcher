"""TrafficWatcherEntity class"""
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import ATTRIBUTION, CONF_PERSON
from .const import DOMAIN
from . import _LOGGER


class TrafficWatcherEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        return f"{DOMAIN}_{slugify(self.name)}"

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.person_name),
            },
            name=self.person_name,
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
        }

    @property
    def person_name(self):
        person_entity = self.config_entry.data.get(CONF_PERSON)
        _LOGGER.warning(self.hass.states.get(person_entity).attributes)
        return self.hass.states.get(person_entity).attributes["friendly_name"]
