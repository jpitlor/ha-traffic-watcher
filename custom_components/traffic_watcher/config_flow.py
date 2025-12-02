"""Adds config flow for Traffic Watcher."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.selector import selector

from .api import TrafficWatcherApiClient
from .const import CONF_PERSON, CONF_HOME, CONF_WORK, CONF_SCHEDULE, DOMAIN, PLATFORMS, CONF_API_KEY


class TrafficWatcherFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for traffic_watcher."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            valid = await self._test_credentials(user_input[CONF_API_KEY])
            if valid:
                return self.async_create_entry(title=user_input[CONF_PERSON], data=user_input)
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return TrafficWatcherOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_PERSON): selector({
                    "entity": {
                        "filter": { "integration": "person" }
                    }
                }),
                vol.Required(CONF_HOME): selector({
                    "entity": {
                        "filter": { "integration": "zone" }
                    }
                }),
                vol.Required(CONF_WORK): selector({
                    "entity": {
                        "filter": { "integration": "zone" }
                    }
                }),
                vol.Required(CONF_SCHEDULE): selector({
                    "entity": {
                        "filter": { "integration": "schedule" }
                    }
                }),
            }),
            errors=self._errors,
        )

    async def _test_credentials(self, api_key):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = TrafficWatcherApiClient(api_key, session)
            await client.async_get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class TrafficWatcherOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for traffic_watcher."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_PERSON), data=self.options
        )
