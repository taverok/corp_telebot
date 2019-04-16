from typing import List, Callable

from bot.models.bot import BotResponse
from bot.models.user import Role


class Route:
    def __init__(self, name: str, handler: object, role: Role, is_public: bool = True):
        self.name = name
        self.handler = handler
        self.role = role
        self.is_public = is_public


routes = {}


def add_handler(name: str, handler: object, role: Role, is_public: bool = True):
    routes.update({name: Route(name, handler, role, is_public)})


def get_handler(name: str, role: Role):
    route: Route = routes.get(name)

    if not route or role.value < route.role.value:
        def empty_handler(*args, **kwargs):
            return BotResponse('404 no route')
        return empty_handler

    return route.handler


def list_handlers(role: Role) -> List[Callable]:
    return [r.handler for r in routes.values() if role.value >= r.role.value]


def list_routes(role: Role, name_starts_with="", only_public: bool = True) -> List[Route]:
    r = [r for r in routes.values()
         if (role.value >= r.role.value)
         & (r.name.lower().startswith(name_starts_with.lower()))]
    if only_public:
        r = [r1 for r1 in r if r1.is_public == True]

    return r


def route_to_help(r: Route):
    if not r or not r.handler:
        return ""

    return (r.name + " - " + r.handler.__doc__).strip()
