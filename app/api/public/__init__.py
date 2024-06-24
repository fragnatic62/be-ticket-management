import os

from fastapi import APIRouter

from app.core.api.base_controller import APIControllerFactory, BaseAPIController
from app.services.authentication.provider import AuthenticationServiceProvider
from app.services.authentication.service import AuthenticationService
from app.services.tm_db.generate_index import MongoDBIndexService

from app.services.tm_db.service import TMMongoDBServicePool


VERSION: str = 'public'

index_service: MongoDBIndexService = MongoDBIndexService()
factory: APIControllerFactory = APIControllerFactory()
tm_db_service_pool: TMMongoDBServicePool = TMMongoDBServicePool()
auth_service_provider: AuthenticationServiceProvider = AuthenticationServiceProvider()

factory.set_mongodb_service_pool(tm_db_service_pool)
auth_service_provider.set_auth_service(AuthenticationService(tm_db_service_pool))

public_router: APIRouter = APIRouter()

dir_path = os.path.dirname(__file__)
controllers = [
    ctrl
    for ctrl in os.listdir(dir_path)
    if os.path.isdir(os.path.join(dir_path, ctrl)) and ctrl != "__pycache__"
]
print('Mounting controllers', controllers)


def route_builder(ctrl: BaseAPIController):
    """
    Builds the API route for the given controller.
    """
    @public_router.api_route(
        ctrl.get_path(),
        methods=[ctrl.get_method()],
        response_model=ctrl.get_response_type(),
        description=ctrl.__doc__,
        tags=ctrl.api_tags
    )
    @index_service.generate_indexes(
        schema=ctrl.get_request_type(),
        service_from_factory=factory
    )
    def handler(req: ctrl.get_request_type()):  # type: ignore[valid-type]
        return ctrl.invoke(req)
    handler.__name__ = f'{ctrl.get_controller_name()}_handler'
    return handler


for controller in controllers:
    """
    Dynamically build the API routes for each controller.
    """
    route_builder(factory.get_controller(controller, VERSION))
