from rest_framework import views, status
from rest_framework.decorators import action
from .. import models
from ..serializers import material_request_serializers, stock_request_serializers
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
        material_requests = material_requests[self.offset : self.endset]
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
        store_id = data.get("store")
        stock_requests = data.get("stock_requests")
        data["user"] = request.user.id

        material_request_serializer = self.serializer_class(data=data)

        if material_request_serializer.is_valid():
            # Crear material request
            material_request_serializer.save()

            # Obetener id de m_r
            material_request = self.get_object(
                material_request_serializer.data.get("id")
            )

            material_request_out_serializer = self.out_serializer_class(
                material_request
            )

            # Array de stocks de salida
            stock_request_out = []

            # Recorrer stock_requests
            for stock_request in stock_requests:
                stock_data = stock_request["stock"]
                stock = models.Stock.objects.filter(id=stock_data["id"]).first()
                if not stock:
                    material_request.delete()
                    return self.response(
                        data={
                            "message": f"Not created, stock does not exist, stock: {stock_data['id']}"
                        },
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )
                if stock_data["new_amount"] > stock.amount:
                    print("new amount")
                    material_request.delete()
                    return self.response(
                        data={
                            "message": f"Not created, amounts over limit, stock amount {stock_data['new_amount']}, stock: {stock.amount}"
                        },
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )
                stock_data["material_request"] = material_request.id
                stock_data["amount"] = stock_data["new_amount"]
                stock_data["stock"] = stock_data["id"]
                stock_request_serializer = (
                    stock_request_serializers.StockRequestSerializer(data=stock_data)
                )
                if stock_request_serializer.is_valid():
                    stock_request_serializer.save()
                    stock_request_out_serializer = (
                        stock_request_serializers.StockRequestOutSerializer(
                            stock_request_serializer.data
                        )
                    )
                    stock_request_out.append(stock_request_out_serializer.data)
                else:
                    material_request.delete()
                    return self.response(
                        data={"errors": stock_request_serializer.errors},
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )
            material_request_out_serializer.data["stock_requests"] = stock_request_out
            for stock_request_out_stock in stock_request_out:
                stock = models.Stock.objects.filter(
                    id=stock_request_out_stock["stock"]
                ).first()   
                print(stock_request_out_stock)
                stock.amount -= stock_request_out_stock["amount"]
                stock.save()
            return self.response(
                data={
                    "material_request": material_request_out_serializer.data,
                    "stock_requests": stock_request_out,
                },
                status=self.status.HTTP_201_CREATED,
            )
        print("last")
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
