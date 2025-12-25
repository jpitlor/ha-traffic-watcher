import json
import logging
from datetime import timedelta
import googlemaps
from google.maps.routing_v2 import RoutesClient, ComputeRoutesRequest, Waypoint, RouteLegStep
from google.oauth2 import service_account

_LOGGER: logging.Logger = logging.getLogger(__package__)
_METERS_IN_MILE = 1609.34


class RoutesResult:
    route: list[str]
    duration: timedelta

    def __init__(self, route: list[str], duration: timedelta):
        self.route = route
        self.duration = duration


class TrafficWatcherApiClient:
    def __init__(self, api_key: str, service_account_json: str) -> None:
        json_acct_info = json.loads(service_account_json)
        credentials = service_account.Credentials.from_service_account_info(json_acct_info)
        self.routes_client = RoutesClient(credentials=credentials)
        self.roads_client = googlemaps.Client(key=api_key)


    def get_road(self, step: RouteLegStep) -> str:
        start = step.start_location.lat_lng
        end = step.end_location.lat_lng
        roads = self.roads_client.snap_to_roads([(start.latitude, start.longitude), (end.latitude, end.longitude)])
        place = self.roads_client.place(roads[len(roads) - 1]['placeId'])
        route_components = list(filter(lambda x: 'route' in x['types'], place['result']['address_components']))
        route_component = route_components[len(route_components) - 1]
        return route_component['short_name'] if "I-" in route_component['short_name'] else route_component['long_name']


    async def get_current_route(self, from_address: str, to_address: str) -> RoutesResult:
        # TODO: traffic aware preference? maybe not available when driving
        request = ComputeRoutesRequest({
            "origin": Waypoint({"address": from_address}),
            "destination": Waypoint({"address": to_address}),
        })
        metadata = [
            ("x-goog-fieldmask", ",".join([
                "routes.legs.duration.seconds",
                "routes.legs.steps.distance_meters",
                "routes.legs.steps.start_location.lat_lng.latitude",
                "routes.legs.steps.start_location.lat_lng.longitude",
                "routes.legs.steps.end_location.lat_lng.latitude",
                "routes.legs.steps.end_location.lat_lng.longitude",
            ]))
        ]
        routes_result = self.routes_client.compute_routes(request, metadata=metadata)

        # We just want point A to point B without alternative routes,
        # so there should be just one route and one leg
        leg = routes_result.routes[0].legs[0]
        major_roads = list(set([self.get_road(step) for step in leg.steps if step.distance_meters > _METERS_IN_MILE]))

        return RoutesResult(major_roads, timedelta(seconds=leg.duration.seconds))

