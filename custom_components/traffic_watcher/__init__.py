import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core_config import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .api import TrafficWatcherApiClient
from .const import CONF_API_KEY, DOMAIN, PLATFORMS, STARTUP_MESSAGE, DATA_LAUNCH_MAPS, DATA_MONTHLY_API_CALLS, \
    DATA_USUAL_ROUTE, DATA_CURRENT_ROUTE, DATA_USUAL_ROUTE_TIME, DATA_CURRENT_ROUTE_TIME, CONF_SERVICE_ACCOUNT_JSON

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)
_DEFAULT_STATE = dict([
    [DATA_LAUNCH_MAPS, False],
    [DATA_MONTHLY_API_CALLS, 0],
    [DATA_USUAL_ROUTE, []],
    [DATA_CURRENT_ROUTE, []],
    [DATA_USUAL_ROUTE_TIME, "0s"],
    [DATA_CURRENT_ROUTE_TIME, "0s"],
])


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    api_key = entry.data.get(CONF_API_KEY)
    service_account_json = entry.data.get(CONF_SERVICE_ACCOUNT_JSON)
    client = TrafficWatcherApiClient(api_key, service_account_json)

    coordinator = TrafficWatcherDataUpdateCoordinator(hass, api_client=client)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.add_update_listener(async_reload_entry)
    await coordinator.async_config_entry_first_refresh()
    return True


class TrafficWatcherDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: TrafficWatcherApiClient,
    ) -> None:
        """Initialize."""
        self.api_client = api_client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL, update_method=self._update_data)

    async def _update_data(self):
        try:
            result = self.data if self.data is not None else _DEFAULT_STATE
            # api_response = await self.api_client.get_current_route()
            # TODO: fetch data from google
            return result
        except Exception as exception:
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
