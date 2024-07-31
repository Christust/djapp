from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models import Q


class HasGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        required_user_types = view.permission_types.get(view.action)
        if required_user_types == None:
            return True
        elif request.user.is_anonymous:
            return False
        elif request.user.user_type == "superadmin":
            return True
        else:
            return request.user.user_type in required_user_types


class BaseGenericViewSet(viewsets.GenericViewSet):
    model = None
    status = status
    out_serializer_class = None
    serializer_class = None
    queryset = None
    permission_classes = [HasGroupPermission]
    permission_types = {}
    searched_object = None
    page = 1
    limit = 100
    offset = 0
    search = ""
    endset = 1
    Q = Q

    def load_paginations(self, request):
        self.search = request.query_params.get("search", "")
        unlimit = request.query_params.get("unlimit", None)
        if unlimit:
            self.page = 1
            self.limit = "unlimit"
            self.offset = 0
            self.endset = None
        else:
            self.page = int(request.query_params.get("page", self.page))
            self.limit = int(request.query_params.get("limit", self.limit))
            self.offset = (self.page * self.limit) - self.limit
            self.endset = self.offset + self.limit

    def get_object(self, pk):
        return get_object_or_404(self.queryset, pk=pk)

    def response(self, data, status=None):
        return Response(
            data=data, status=status if status is not None else self.status.HTTP_200_OK
        )

    def dummy_response(self):
        return self.response(data={"dummy": "dummy"})


class BaseModelViewSet(viewsets.ModelViewSet):
    model = None
    status = status
    out_serializer_class = None
    serializer_class = None
    queryset = None
    permission_classes = [HasGroupPermission]
    permission_types = {}
    searched_object = None
    page = 1
    limit = 100
    offset = 0
    search = ""
    endset = 1
    Q = Q

    def load_paginations(self, request):
        self.search = request.query_params.get("search", "")
        unlimit = request.query_params.get("unlimit", None)
        if unlimit:
            self.page = 1
            self.limit = "unlimit"
            self.offset = 0
            self.endset = None
        else:
            self.page = int(request.query_params.get("page", self.page))
            self.limit = int(request.query_params.get("limit", self.limit))
            self.offset = (self.page * self.limit) - self.limit
            self.endset = self.offset + self.limit

    def get_object(self, pk):
        return get_object_or_404(self.queryset, pk=pk)

    def response(self, data, status):
        return Response(
            data=data, status=status if status is not None else self.status.HTTP_200_OK
        )
