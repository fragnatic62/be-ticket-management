from http import HTTPMethod
from typing import List

from pymongo.collection import Collection

from app.api.v1.fetch_companies.models import FetchCompaniesResponse, Task, Board, Company, FetchCompaniesRequest
from app.core.api.base_controller import BaseAPIController
from app.core.api.collections import DBCollectionEnum
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[FetchCompaniesRequest, FetchCompaniesResponse],
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
        return '/fetch_companies'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def _get_tasks(self, board_id: str) -> List[Task]:
        """
        Get the list of tasks.
        """
        nosql_service: Collection = self.get_mongodb_service_from_collection(DBCollectionEnum.TASKS.value)
        q_response = nosql_service.find({'board_id': board_id})

        tasks: List[Task] = [
            Task(
                id=str(task.get('_id')),
                position=task.get('position'),
                name=task.get('name'),
                description=task.get('description'),
                board_id=task.get('board_id'),
                date_created=task.get('date_created'),
                date_updated=task.get('date_updated')
            )
            for task in q_response
        ]
        return tasks

    def _get_boards(self, company_id: str) -> List[Board]:
        """
        Get the list of boards.
        """
        nosql_service: Collection = self.get_mongodb_service_from_collection(DBCollectionEnum.BOARDS.value)
        q_response = nosql_service.find({'company_id': company_id})

        boards: List[Board] = [
            Board(
                id=str(board.get('_id')),
                position=board.get('position'),
                name=board.get('name'),
                description=board.get('description'),
                company_id=board.get('company_id'),
                tasks=self._get_tasks(board_id=str(board.get('_id')))
            )
            for board in q_response
        ]

        return boards

    def process_request(self, request: FetchCompaniesRequest) -> FetchCompaniesResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(DBCollectionEnum.COMPANIES.value)
            total_count = nosql_service.count_documents({})
            q_response = nosql_service.find().skip((request.page - 1) * request.page_size).limit(request.page_size)

            companies: List[Company] = [
                Company(
                    id=str(company.get('_id')),
                    name=company.get('name'),
                    email=company.get('email'),
                    description=company.get('description'),
                    boards=self._get_boards(company_id=str(company.get('_id'))),
                    date_created=company.get('date_created'),
                    date_updated=company.get('date_updated')
                )
                for company in q_response
            ]

            return FetchCompaniesResponse(
                results=companies,
                page=request.page,
                page_size=request.page_size,
                total_count=total_count
            )
        except Exception as e:
            raise e

    def validate_request(self, request: FetchCompaniesRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        return True
