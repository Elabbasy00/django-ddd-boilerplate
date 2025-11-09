from collections import OrderedDict

from django.test import TestCase
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from src.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from src.users.models import User
from src.infrastructure.dependency_injection.container import get_container
from src.application.shared.dtos import UserCreateDTO


class ExampleListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "email")

    def get(self, request):
        queryset = User.objects.order_by("id")

        response = get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )

        return response


class GetPaginatedResponseTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        container = get_container()
        user1_dto = container.create_user_use_case.execute(
            UserCreateDTO(username="Ahmed", password="123456", email="user1@hacksoft.io")
        )
        user2_dto = container.create_user_use_case.execute(
            UserCreateDTO(username="Ahmed2", password="123456", email="user2@hacksoft.io")
        )
        from src.users.models import User

        self.user1 = User.objects.get(id=user1_dto.id)
        self.user2 = User.objects.get(id=user2_dto.id)

    def test_response_is_paginated_correctly(self):
        first_page_request = self.factory.get("/some/path")
        first_page_response = ExampleListApi.as_view()(first_page_request)

        expected_first_page_response = OrderedDict(
            {
                "limit": 1,
                "offset": 0,
                "count": User.objects.count(),
                "next": "http://testserver/some/path?limit=1&offset=1",
                "previous": None,
                "results": [
                    OrderedDict(
                        {
                            "id": self.user1.id,
                            "email": self.user1.email,
                        }
                    )
                ],
            }
        )

        self.assertEqual(expected_first_page_response, first_page_response.data)

        next_page_request = self.factory.get("/some/path?limit=1&offset=1")
        next_page_response = ExampleListApi.as_view()(next_page_request)

        expected_next_page_response = OrderedDict(
            {
                "limit": 1,
                "offset": 1,
                "count": User.objects.count(),
                "next": None,
                "previous": "http://testserver/some/path?limit=1",
                "results": [
                    OrderedDict(
                        {
                            "id": self.user2.id,
                            "email": self.user2.email,
                        }
                    )
                ],
            }
        )

        self.assertEqual(expected_next_page_response, next_page_response.data)
