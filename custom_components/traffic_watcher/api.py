import json
import logging
from datetime import timedelta

from google.oauth2 import service_account
from google.maps.routing_v2 import RoutesClient

TIMEOUT = 10
_LOGGER: logging.Logger = logging.getLogger(__package__)
HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class RoutesResult:
    route: list[str]
    duration: timedelta


class TrafficWatcherApiClient:
    def __init__(self, api_key: str) -> None:
        json_acct_info = json.loads(api_key)
        credentials = service_account.Credentials.from_service_account_info(json_acct_info)
        self.client = RoutesClient(credentials=credentials)

    async def get_current_route(self, from_address: str, to_address: str) -> RoutesResult:
        x = self.client.compute_routes()
        x.routes.pop(
