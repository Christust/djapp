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
        store = self.request.query_params.get("store", None)
        branch = self.request.query_params.get("branch", None)
        exclude = request.query_params.getlist("exclude[]")
        only_existences = request.query_params.get("only_existences", False)
        self.load_paginations(request)

        if store:
            stocks = self.queryset.filter(store_id=store)
        else:
            stocks = self.queryset
        if branch:
            stocks = stocks.filter(store__branch__id=branch)
        if only_existences:
            stocks = stocks.exclude(amount=0)

        stocks = stocks.filter(
            self.Q(item__name__icontains=self.search)
            | self.Q(store__name__icontains=self.search)
            | self.Q(store__branch__name__icontains=self.search)
        ).exclude(id__in=exclude)
        stocks_count = stocks.count()
        stocks = stocks[self.offset : self.endset]
        stocks_out_serializer = self.out_serializer_class(stocks, many=True)
        stock_items = []
        for stock in stocks_out_serializer.data:
            stock_item = {
                "id": stock["id"],
                "item": stock["item"]["name"],
                "amount": stock["amount"],
            }
            stock_items.append(stock_item)
        return self.response(
            data={
                "stocks": stocks_out_serializer.data,
                "stock_items": stock_items,
                "total": stocks_count,
                "limit": self.limit,
            },
            status=self.status.HTTP_200_OK,
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
        stock_serializer = self.serializer_class(stock, data=request.data, partial=True)
        if stock_serializer.is_valid():
            stock_serializer.save()
            stock = self.get_object(pk)
            stock_out_serializer = self.out_serializer_class(stock)
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
