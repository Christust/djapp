from rest_framework import views, status
from rest_framework.decorators import action
from .. import models
from ..serializers import stock_serializers
from apps.base.views import BaseGenericViewSet


class StockViewSet(BaseGenericViewSet):
    model = models.Stock
    serializer_class = stock_serializers.StockSerializer
    out_serializer_class = stock_serializers.StockOutSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_types = {
        "list": ["admin"],
        "retrieve": ["admin"],
        "create": ["admin"],
        "update": ["admin"],
        "delete": ["admin"],
    }

    def list(self, request):
        offset = int(self.request.query_params.get("offset", 0))
        limit = int(self.request.query_params.get("limit", 10))

        stocks = self.queryset.all()[offset : offset + limit]
        stocks_out_serializer = self.out_serializer_class(stocks, many=True)
        return self.response(
            data=stocks_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def create(self, request):
        stock_serializer = self.serializer_class(data=request.data)
        if stock_serializer.is_valid():
            stock_serializer.save()
            stock = self.get_object(stock_serializer.data.get("id"))
            stock_out_serializer = self.out_serializer_class(stock)
            return self.response(
                data=stock_out_serializer.data, status=self.status.HTTP_201_CREATED
            )
        return self.response(
            data=stock_serializer.errors, status=self.status.HTTP_406_NOT_ACCEPTABLE
        )

    def retrieve(self, request, pk):
        stock = self.get_object(pk)
        stock_out_serializer = self.out_serializer_class(stock)
        return self.response(
            data=stock_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def update(self, request, pk):
        stock = self.get_object(pk)
        stock_out_serializer = self.out_serializer_class(
            stock, data=request.data, partial=True
        )
        if stock_out_serializer.is_valid():
            stock_out_serializer.save()
            return self.response(
                data=stock_out_serializer.data, status=self.status.HTTP_202_ACCEPTED
            )
        return self.response(
            data=stock_out_serializer.errors, status=self.status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        stock = self.get_object(pk)
        stock.delete()
        return self.response(
            data={"message": "Deleted"}, status=self.status.HTTP_200_OK
        )
