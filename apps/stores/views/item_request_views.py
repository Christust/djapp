from rest_framework import views, status
from rest_framework.decorators import action
from .. import models
from ..serializers import item_request_serializers
from apps.base.views import BaseGenericViewSet


class ItemRequestViewSet(BaseGenericViewSet):
    model = models.ItemRequest
    serializer_class = item_request_serializers.ItemRequestSerializer
    out_serializer_class = item_request_serializers.ItemRequestOutSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)
    permission_types = {
        "list": ["admin"],
        "retrieve": ["admin"],
        "create": ["admin"],
        "update": ["admin"],
        "delete": ["admin"],
    }

    def list(self, request):
        self.load_paginations(request)

        item_requests = self.queryset
        item_requests_count = item_requests.count()
        item_requests = item_requests[self.offset : self.offset + self.limit]
        item_requests_out_serializer = self.out_serializer_class(
            item_requests, many=True
        )
        return self.response(
            data={
                "item_requests": item_requests_out_serializer.data,
                "total": item_requests_count,
                "limit": self.limit,
            },
            status=self.status.HTTP_200_OK,
        )

    def create(self, request):
        item_request_serializer = self.serializer_class(data=request.data)
        if item_request_serializer.is_valid():
            item_request_serializer.save()
            item_request = self.get_object(item_request_serializer.data.get("id"))
            item_request_out_serializer = self.out_serializer_class(item_request)
            return self.response(
                data=item_request_out_serializer.data,
                status=self.status.HTTP_201_CREATED,
            )
        return self.response(
            data=item_request_serializer.errors,
            status=self.status.HTTP_406_NOT_ACCEPTABLE,
        )

    def retrieve(self, request, pk):
        item_request = self.get_object(pk)
        item_request_out_serializer = self.out_serializer_class(item_request)
        return self.response(
            data=item_request_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def update(self, request, pk):
        item_request = self.get_object(pk)
        item_request_out_serializer = self.out_serializer_class(
            item_request, data=request.data, partial=True
        )
        if item_request_out_serializer.is_valid():
            item_request_out_serializer.save()
            return self.response(
                data=item_request_out_serializer.data,
                status=self.status.HTTP_202_ACCEPTED,
            )
        return self.response(
            data=item_request_out_serializer.errors,
            status=self.status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk):
        item_request = self.get_object(pk)
        item_request.delete()
        item_request.save()
        return self.response(
            data={"message": "Deleted"}, status=self.status.HTTP_200_OK
        )
