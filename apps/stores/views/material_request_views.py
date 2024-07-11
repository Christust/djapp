from rest_framework import views, status
from rest_framework.decorators import action
from .. import models
from ..serializers import material_request_serializers, item_request_serializers
from apps.base.views import BaseGenericViewSet


class MaterialRequestViewSet(BaseGenericViewSet):
    model = models.MaterialRequest
    serializer_class = material_request_serializers.MaterialRequestSerializer
    out_serializer_class = material_request_serializers.MaterialRequestOutSerializer
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

        material_requests = self.queryset
        material_requests_count = material_requests.count()
        material_requests = material_requests[self.offset : self.offset + self.limit]
        material_requests_out_serializer = self.out_serializer_class(
            material_requests, many=True
        )
        return self.response(
            data={
                "material_requests": material_requests_out_serializer.data,
                "total": material_requests_count,
                "limit": self.limit,
            },
            status=self.status.HTTP_200_OK,
        )

    def create(self, request):
        data = request.data
        data["user"] = request.user.id
        material_request_serializer = self.serializer_class(data=data)
        if material_request_serializer.is_valid():
            material_request_serializer.save()
            material_request = self.get_object(
                material_request_serializer.data.get("id")
            )
            store_id = material_request.store
            material_request_out_serializer = self.out_serializer_class(
                material_request
            )

            item_requests = data.get("item_requests")
            item_request_out = []
            for item_request in item_requests:
                item_id = item_request.get("item")
                stock = models.Stock.objects.filter(
                    store=store_id, item=item_id
                ).first()
                if not stock:
                    material_request.delete()
                    return self.response(
                        data={
                            "message": f"Not created, stock does not exist, item: {item_id}"
                        },
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )
                if item_request.get("amount") > stock.amount:
                    material_request.delete()
                    return self.response(
                        data={
                            "message": f"Not created, amounts over limit, item amount {item_request.get('amount')}, stock: {stock.amount}"
                        },
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )
                item_request["material_request"] = material_request.id
                item_request_serializer = (
                    item_request_serializers.ItemRequestSerializer(data=item_request)
                )
                if item_request_serializer.is_valid():
                    item_request_serializer.save()
                    item_request_out_serializer = (
                        item_request_serializers.ItemRequestOutSerializer(
                            item_request_serializer.data
                        )
                    )
                    item_request_out.append(item_request_out_serializer.data)
                else:
                    material_request.delete()
                    return self.response(
                        data={"message": "Not created"},
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )
            material_request_out_serializer.data["item_requests"] = item_request_out
            for item_request_out_item in item_request_out:
                stock = models.Stock.objects.filter(
                    store=store_id, item=item_request_out_item["item"]
                ).first()
                stock.amount -= item_request_out_item["amount"]
                stock.save()
            return self.response(
                data={
                    "material_request": material_request_out_serializer.data,
                    "item_requests": item_request_out,
                },
                status=self.status.HTTP_201_CREATED,
            )
        return self.response(
            data=material_request_serializer.errors,
            status=self.status.HTTP_406_NOT_ACCEPTABLE,
        )

    def retrieve(self, request, pk):
        material_request = self.get_object(pk)
        material_request_out_serializer = self.out_serializer_class(material_request)
        return self.response(
            data=material_request_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def update(self, request, pk):
        material_request = self.get_object(pk)
        material_request_out_serializer = self.out_serializer_class(
            material_request, data=request.data, partial=True
        )
        if material_request_out_serializer.is_valid():
            material_request_out_serializer.save()
            return self.response(
                data=material_request_out_serializer.data,
                status=self.status.HTTP_202_ACCEPTED,
            )
        return self.response(
            data=material_request_out_serializer.errors,
            status=self.status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk):
        material_request = self.get_object(pk)
        material_request.delete()
        return self.response(
            data={"message": "Deleted"}, status=self.status.HTTP_200_OK
        )
