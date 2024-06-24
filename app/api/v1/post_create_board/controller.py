from http import HTTPMethod
from typing import List

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.api.v1.post_create_board.exceptions import PostCreateBoardException, CreateBoardException
from app.api.v1.post_create_board.models import PostCreateBoardRequest, PostCreateBoardResponse
from app.core.api.base_controller import BaseAPIController
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[PostCreateBoardRequest, PostCreateBoardResponse],
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
        return '/post_create_board'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def process_request(self, request: PostCreateBoardRequest) -> PostCreateBoardResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            inserted_board_id = nosql_service.insert_one(request.model_dump()).inserted_id.__str__()

            return PostCreateBoardResponse(
                id=inserted_board_id,
                name=request.name,
                description=request.description,
                company_id=request.company_id,
                position=request.position,
                date_created=request.date_created,
                date_updated=request.date_updated,
            )
        except DuplicateKeyError:
            raise PostCreateBoardException('Board already exists.')

        except Exception as e:
            raise CreateBoardException(str(e))

    def validate_request(self, request: PostCreateBoardRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        return True
