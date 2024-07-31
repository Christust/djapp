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

        material_requests = self.queryset.order_by("id").reverse()
        material_requests_count = material_requests.count()
        material_requests = material_requests[self.offset : self.endset]
        material_requests_array = []
        for material_request in material_requests:
            stock_requests = models.StockRequest.objects.filter(
                material_request=material_request.id
            )
            stock_requests_array = []
            for stock_request in stock_requests:
                stock_requests_array.append(
                    {
                        "stock": {
                            "id": stock_request.stock.id,
                            "item": stock_request.stock.item.name,
                            "amount": stock_request.amount,
                            "new_amount": 0,
                        }
                    }
                )
            material_request_object = {
                "id": material_request.id,
                "store": material_request.store.id,
                "user": material_request.user.full_name,
                "finished": material_request.finished,
                "granted": material_request.granted,
                "branch": material_request.store.branch.id,
                "store_name": material_request.store.name,
                "stock_requests": stock_requests_array,
            }
            material_requests_array.append(material_request_object)
            """
            {
            'branch': 1,
            'store': 1,
            'stock_requests': [
                    {
                        'stock': {
                            'id': 1,
                            'item': 'Pinol',
                            'amount': 15,
                            'new_amount': 11
                        }
                    },
                    {
                        'stock': {
                            'id': 3,
                            'item': 'Escoba',
                            'amount': 2,
                            'new_amount': 2
                        }
                    }
                ]
            }
            """
        return self.response(
            data={
                "material_requests": material_requests_array,
                "total": material_requests_count,
                "limit": self.limit,
            },
            status=self.status.HTTP_200_OK,
        )

    def create(self, request):
        data = request.data
        """
            {
            'branch': 1,
            'store': 1,
            'stock_requests': [
                        {
                        'stock': {
                            'id': 1,
                            'item': 'Pinol',
                            'amount': 15,
                            'new_amount': 11
                            }
                        }, 
                        {
                        'stock': {
                            'id': 3,
                            'item': 'Escoba',
                            'amount': 2,
                            'new_amount': 2
                        }
                    }
                ]
            }
        """
        # Obtenemos los stocks a modificar
        stock_requests = data.get("stock_requests")

        # Obtenemos el usuario que hace la peticion
        data["user"] = request.user.id

        # Serializamos los datos necesarios para crear una peticion de material
        material_request_serializer = self.serializer_class(data=data)

        # Verificamos si es valido los datos de la peticion de material
        if material_request_serializer.is_valid():

            # Crear material request
            material_request_serializer.save()

            # Obetener el nuevo material request para serializarlo de salida
            material_request = self.get_object(
                material_request_serializer.data.get("id")
            )

            # Serializar de salida
            material_request_out_serializer = self.out_serializer_class(
                material_request
            )

            # Array de stocks de salida (opcional)
            stock_request_out = []

            # Recorrer stocks a cambiar
            for stock_request in stock_requests:

                # Tomamos el stock solicitado
                stock_data = stock_request["stock"]

                # Buscamos el stock por id
                stock = models.Stock.objects.filter(id=stock_data["id"]).first()

                # Si el stock no existe mandamos error
                if not stock:
                    material_request.delete()
                    return self.response(
                        data={
                            "message": f"Not created, stock does not exist, stock: {stock_data['id']}"
                        },
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )

                # Si el nuevo monto es mayor al del stock mandamos error
                if stock_data["new_amount"] > stock.amount:
                    print("new amount")
                    material_request.delete()
                    return self.response(
                        data={
                            "message": f"Not created, amounts over limit, stock amount {stock_data['new_amount']}, stock: {stock.amount}"
                        },
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )

                # Enlazamos el stock request con su material request (antes creado)
                stock_data["material_request"] = material_request.id

                # Usamos el monto nuevo
                stock_data["amount"] = stock_data["new_amount"]

                # Enlazamos el stock request a un stock
                stock_data["stock"] = stock_data["id"]

                # Serializamos la informacion
                stock_request_serializer = (
                    stock_request_serializers.StockRequestSerializer(data=stock_data)
                )

                # Verificamos si es valido
                if stock_request_serializer.is_valid():

                    # Guardamos
                    stock_request_serializer.save()

                    # Serializamos de salida
                    stock_request_out_serializer = (
                        stock_request_serializers.StockRequestOutSerializer(
                            stock_request_serializer.data
                        )
                    )

                    # Agregamos cada uno de los stock request al array previo
                    stock_request_out.append(stock_request_out_serializer.data)
                else:
                    material_request.delete()
                    return self.response(
                        data={"errors": stock_request_serializer.errors},
                        status=self.status.HTTP_406_NOT_ACCEPTABLE,
                    )

            # Agregamos el array al objecto de salida
            material_request_out_serializer.data["stock_requests"] = stock_request_out

            # Recorremos cada uno de los stock request creados correctamente para
            # finalmente actualizar los stock existentes
            for stock_request_out_stock in stock_request_out:

                # Obtenemos el stock
                stock = models.Stock.objects.filter(
                    id=stock_request_out_stock["stock"]
                ).first()

                # Actualizamos la cantidad
                stock.amount -= stock_request_out_stock["amount"]

                # Guardamos
                stock.save()

            # Respondemos con toda la informacion generada
            return self.response(
                data={
                    "material_request": material_request_out_serializer.data,
                    "stock_requests": stock_request_out,
                },
                status=self.status.HTTP_201_CREATED,
            )

        # Respuesta de material no valido
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
        """
        {
        'branch': 1,
        'store': 1,
        'all_material': true
        'stock_requests': [
                    {
                    'stock': {
                        'id': 1,
                        'item': 'Pinol',
                        'amount': 15,
                        'new_amount': 11
                        }
                    },
                    {
                    'stock': {
                        'id': 3,
                        'item': 'Escoba',
                        'amount': 2,
                        'new_amount': 2
                    }
                }
            ]
        }
        """

        # Obtenemos el material request
        material_request = self.get_object(pk)

        if material_request.finished:
            return self.response(
                data={"error": "Material request finished"},
                status=self.status.HTTP_400_BAD_REQUEST,
            )

        data = request.data
        stock_requests = data["stock_requests"]

        # Recorremos los stock a modificar
        for stock_request in stock_requests:

            # Obtenemos los datos necesarios para localizar los stock request
            stock_data = stock_request["stock"]
            stock_id = stock_data["id"]

            # Obtenemos el stock request a modificar
            editable_stock_request = models.StockRequest.objects.filter(
                stock=stock_id, material_request=material_request.id
            ).first()

            # Verificamos que exista
            if editable_stock_request is None:
                # No existe el stock request
                return self.response(
                    data={"error": "Stock not exist"},
                    status=self.status.HTTP_400_BAD_REQUEST,
                )

        for stock_request in stock_requests:

            # Obtenemos los datos necesarios para localizar los stock request
            stock_data = stock_request["stock"]
            amount = stock_data["amount"]
            amount_returned = stock_data["new_amount"]
            stock_id = stock_data["id"]

            # Obtenemos el stock request a modificar
            editable_stock_request = models.StockRequest.objects.filter(
                stock=stock_id, material_request=material_request.id
            ).first()

            # Validamos si el monto es igual al monto registrado
            if editable_stock_request.amount != amount:
                return self.response(
                    data={"error": "Amount does not match"},
                    status=self.status.HTTP_400_BAD_REQUEST,
                )

            # Validamos que el monto a retornar no sea mayor al monto registrado
            if amount_returned > editable_stock_request.amount:
                return self.response(
                    data={"error": "Amount returned over amount"},
                    status=self.status.HTTP_400_BAD_REQUEST,
                )

            # Actualizamos
            editable_stock_request.amount_returned = amount_returned
            editable_stock_request.save()

            stock = models.Stock.objects.filter(id=stock_id).first()
            stock.amount += amount_returned
            stock.save()

        material_request.finished = True
        material_request.granted = True
        material_request.save()

        material_request_out_serializer = self.out_serializer_class(material_request)
        return self.response(
            data=material_request_out_serializer.data,
            status=self.status.HTTP_202_ACCEPTED,
        )

    def destroy(self, request, pk):
        material_request = self.get_object(pk)
        material_request.delete()
        return self.response(
            data={"message": "Deleted"}, status=self.status.HTTP_200_OK
        )
