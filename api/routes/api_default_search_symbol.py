from flask_restful import Resource
from requests import Response

from api.biz.search_engine.search_symbol_service import SearchSymbolService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiDefaultSearchSymbol(Resource):

    @inject_service()
    def __init__(self, search_symbol_service: SearchSymbolService) -> None:
        self._search_symbol_service = search_symbol_service

    def get(self) -> Response:
        data = self._search_symbol_service.default_search()
        return api_response(data=data, message="Success")
