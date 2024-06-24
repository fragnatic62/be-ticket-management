from http import HTTPMethod
from typing import List

from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from app.api.v1.post_update_board.exceptions import PostUpdateBoardException, UpdateBoardException
from app.api.v1.post_update_board.models import PostUpdateBoardRequest, PostUpdateBoardResponse
from app.core.api.base_controller import BaseAPIController
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[PostUpdateBoardRequest, PostUpdateBoardResponse],
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
        return '/post_update_board'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def process_request(self, request: PostUpdateBoardRequest) -> PostUpdateBoardResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            q_response = nosql_service.update_one(
                {'_id': request.id},
                {
                    '$set': {
                        'position': request.position,
                        'name': request.name,
                        'description': request.description,
                        'date_updated': request.date_updated
                    }
                }
            )

            if q_response.modified_count == 0:
                raise PostUpdateBoardException('No record updated.')

            return PostUpdateBoardResponse(
                id=request.id,
                position=request.position,
                name=request.name,
                description=request.description,
                company_id=request.company_id,
                date_created=request.date_created,
                date_updated=request.date_updated
            )
        except OperationFailure:
            raise PostUpdateBoardException('Error occurred during updating board.')

        except Exception as e:
            raise UpdateBoardException(str(e))

    def validate_request(self, request: PostUpdateBoardRequest) -> bool:
        """
        Validate the request
        """
        return True
