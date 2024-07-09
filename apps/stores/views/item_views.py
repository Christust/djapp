from .. import models
from ..serializers import item_serializers
from apps.base.views import BaseGenericViewSet
from django.db.models import Q


class ItemViewSet(BaseGenericViewSet):
    model = models.Item
    serializer_class = item_serializers.ItemSerializer
    out_serializer_class = item_serializers.ItemOutSerializer
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
        search = request.query_params.get("search", "")

        items = self.queryset.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
        items_count = items.count()
        items = items[self.offset : self.offset + self.limit]
        items_out_serializer = self.out_serializer_class(items, many=True)
        return self.response(
            data={
                "items": items_out_serializer.data,
                "total": items_count,
                "limit": self.limit,
            },
            status=self.status.HTTP_200_OK,
        )

    def create(self, request):
        item_serializer = self.serializer_class(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            item = self.get_object(item_serializer.data.get("id"))
            item_out_serializer = self.out_serializer_class(item)
            return self.response(
                data=item_out_serializer.data, status=self.status.HTTP_201_CREATED
            )
        return self.response(
            data=item_serializer.errors, status=self.status.HTTP_406_NOT_ACCEPTABLE
        )

    def retrieve(self, request, pk):
        item = self.get_object(pk)
        item_out_serializer = self.out_serializer_class(item)
        return self.response(
            data=item_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def update(self, request, pk):
        item = self.get_object(pk)
        item_out_serializer = self.out_serializer_class(
            item, data=request.data, partial=True
        )
        if item_out_serializer.is_valid():
            item_out_serializer.save()
            return self.response(
                data=item_out_serializer.data, status=self.status.HTTP_202_ACCEPTED
            )
        return self.response(
            data=item_out_serializer.errors, status=self.status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        item = self.get_object(pk)
        item.is_active = False
        item.save()
        return self.response(
            data={"message": "Deleted"}, status=self.status.HTTP_200_OK
        )
