from rest_framework import views, status
from rest_framework.decorators import action
from apps.branches import serializers, models
from apps.base.views import BaseGenericViewSet


class BranchViewSet(BaseGenericViewSet):
    model = models.Branch
    serializer_class = serializers.BranchSerializer
    out_serializer_class = serializers.BranchOutSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)
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

        branches = self.queryset.all()[offset : offset + limit]
        branches_out_serializer = self.out_serializer_class(branches, many=True)
        return self.response(
            data=branches_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def create(self, request):
        branch_serializer = self.serializer_class(data=request.data)
        if branch_serializer.is_valid():
            branch_serializer.save()
            branch = self.get_object(branch_serializer.data.get("id"))
            branch_out_serializer = self.out_serializer_class(branch)
            return self.response(
                data=branch_out_serializer.data, status=self.status.HTTP_201_CREATED
            )
        return self.response(
            data=branch_serializer.errors, status=self.status.HTTP_406_NOT_ACCEPTABLE
        )

    def retrieve(self, request, pk):
        branch = self.get_object(pk)
        branch_out_serializer = self.out_serializer_class(branch)
        return self.response(
            data=branch_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def update(self, request, pk):
        branch = self.get_object(pk)
        branch_out_serializer = self.out_serializer_class(
            branch, data=request.data, partial=True
        )
        if branch_out_serializer.is_valid():
            branch_out_serializer.save()
            return self.response(
                data=branch_out_serializer.data, status=self.status.HTTP_202_ACCEPTED
            )
        return self.response(
            data=branch_out_serializer.errors, status=self.status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        branch = self.get_object(pk)
        branch.is_active = False
        branch.save()
        return self.response(
            data={"message": "Deleted"}, status=self.status.HTTP_200_OK
        )


class CountryViewSet(BaseGenericViewSet):
    model = models.Country
    serializer_class = serializers.CountrySerializer
    out_serializer_class = serializers.CountrySerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)
    permission_types = {
        "list": ["admin"],
        "retrieve": ["admin"],
    }

    def list(self, request):
        offset = int(self.request.query_params.get("offset", 0))
        limit = int(self.request.query_params.get("limit", 10))

        countries = self.queryset.all()[offset : offset + limit]
        countries_out_serializer = self.out_serializer_class(countries, many=True)
        return self.response(
            data=countries_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        country = self.get_object(pk)
        country_out_serializer = self.out_serializer_class(country)
        return self.response(
            data=country_out_serializer.data, status=self.status.HTTP_200_OK
        )


class StateViewSet(BaseGenericViewSet):
    model = models.State
    serializer_class = serializers.StateSerializer
    out_serializer_class = serializers.StateSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)
    permission_types = {
        "list": ["admin"],
        "retrieve": ["admin"],
    }

    def list(self, request):
        offset = int(self.request.query_params.get("offset", 0))
        limit = int(self.request.query_params.get("limit", 10))

        states = self.queryset.all()[offset : offset + limit]
        states_out_serializer = self.out_serializer_class(states, many=True)
        return self.response(
            data=states_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        state = self.get_object(pk)
        state_out_serializer = self.out_serializer_class(state)
        return self.response(
            data=state_out_serializer.data, status=self.status.HTTP_200_OK
        )


class CityViewSet(BaseGenericViewSet):
    model = models.City
    serializer_class = serializers.CitySerializer
    out_serializer_class = serializers.CitySerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)
    permission_types = {
        "list": ["admin"],
        "retrieve": ["admin"],
    }

    def list(self, request):
        offset = int(self.request.query_params.get("offset", 0))
        limit = int(self.request.query_params.get("limit", 10))

        cities = self.queryset.all()[offset : offset + limit]
        cities_out_serializer = self.out_serializer_class(cities, many=True)
        return self.response(
            data=cities_out_serializer.data, status=self.status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        city = self.get_object(pk)
        city_out_serializer = self.out_serializer_class(city)
        return self.response(
            data=city_out_serializer.data, status=self.status.HTTP_200_OK
        )
