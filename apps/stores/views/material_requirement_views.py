from rest_framework import views, status
from rest_framework.decorators import action
from .. import models
from ..serializers import store_serializers
from apps.base.views import BaseGenericViewSet

class StoreViewSet(BaseGenericViewSet):
    model = models.Store
    serializer_class = store_serializers.StoreSerializer
    out_serializer_class = store_serializers.StoreOutSerializer
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

        stores = self.queryset
        stores_count = stores.count()
        stores = stores[self.offset : self.offset + self.limit]
        stores_out_serializer = self.out_serializer_class(stores, many=True)
        return self.response(
            data={
                "stores": stores_out_serializer.data,
                "total": stores_count,
                "limit": self.limit,
            },
            status=self.status.HTTP_200_OK,
        )

    def create(self, request):
        store_serializer = self.serializer_class(data=request.data)
        if store_serializer.is_valid():
            store_serializer.save()
            store = self.get_object(store_serializer.data.get("id"))
            store_out_serializer = self.out_serializer_class(store)
            return self.response(
                data=store_out_serializer.data, status=self.status.HTTP_201_CREATED
            )
        return self.response(
            data=store_serializer.errors, status=self.status.HTTP_406_NOT_ACCEPTABLE
        )

    def retrieve(self, request, pk):
        store = self.get_object(pk)
        store_out_serializer = self.out_serializer_class(store)
        return self.response(
            data=store_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def update(self, request, pk):
        store = self.get_object(pk)
        store_out_serializer = self.out_serializer_class(
            store, data=request.data, partial=True
        )
        if store_out_serializer.is_valid():
            store_out_serializer.save()
            return self.response(
                data=store_out_serializer.data, status=self.status.HTTP_202_ACCEPTED
            )
        return self.response(
            data=store_out_serializer.errors, status=self.status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        store = self.get_object(pk)
        store.is_active = False
        store.save()
        return self.response(
            data={"message": "Deleted"}, status=self.status.HTTP_200_OK
        )