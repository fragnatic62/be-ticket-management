from http import HTTPMethod
from typing import List

from pymongo.collection import Collection

from app.api.v1.post_create_company.models import PostCreateCompanyRequest, PostCreateCompanyResponse
from app.core.api.base_controller import BaseAPIController
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[PostCreateCompanyRequest, PostCreateCompanyResponse],
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
        return '/post_create_company'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def process_request(self, request: PostCreateCompanyRequest) -> PostCreateCompanyResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            inserted_company_id = nosql_service.insert_one(request.model_dump()).inserted_id.__str__()

            return PostCreateCompanyResponse(
                id=inserted_company_id,
                name=request.name,
                email=request.email,
                description=request.description,
                date_created=request.date_created,
                date_updated=request.date_updated
            )
        except Exception as e:
            raise e

    def validate_request(self, request: PostCreateCompanyRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        return True
