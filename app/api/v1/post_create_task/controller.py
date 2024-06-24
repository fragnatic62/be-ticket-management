from http import HTTPMethod
from typing import List

from pymongo.collection import Collection

from app.api.v1.post_create_task.models import PostCreateTaskResponse, PostCreateTasksRequest
from app.core.api.base_controller import BaseAPIController
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[PostCreateTasksRequest, PostCreateTaskResponse],
    TMMongoDBServiceProvider
):
    """
    **Synchronous API endpoint for fetching completeness summary**

    API request attributes:
        schedule_date (date): The date of the schedule.
        retailers (Array[str]): The list of retailers. e.g. ['amazon.com', 'walmart.com']

    """
    _full_dir: str = __file__
    api_tags: List[str] = ['Synchronous API']

    def get_path(self) -> str:
        return '/post_create_task'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def process_request(self, request: PostCreateTasksRequest) -> PostCreateTaskResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            inserted_task_id = nosql_service.insert_one(request.model_dump()).inserted_id.__str__()

            return PostCreateTaskResponse(
                id=inserted_task_id,
                position=request.position,
                name=request.name,
                description=request.description,
                board_id=request.board_id,
                date_created=request.date_created,
                date_updated=request.date_updated
            )
        except Exception as e:
            raise e

    def validate_request(self, request: PostCreateTasksRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        return True
