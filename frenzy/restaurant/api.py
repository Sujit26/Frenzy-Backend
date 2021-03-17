from rest_framework import viewsets, mixins, response
from django_filters import rest_framework as df_filters

from frenzy.restaurant import models, serializers, filters
from frenzy.user import models as TxnModels


class RestaurantAPI(
    # mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.RestaurantSerializers
    filter_backends = [df_filters.DjangoFilterBackend]
    filterset_class = filters.RestaurantFilter

    def get_queryset(self):
        nod = int(self.request.query_params.get('nod', '-1'))
        min_price = float(self.request.query_params.get('min_price', '0'))
        max_price = float(self.request.query_params.get('max_price', '999999'))
        mode = self.request.query_params.get('mode', 'lte')
        if nod != -1:
            open_restaurants_ids = [
                res.id for res in models.Restaurant.objects.all() if models.dishes_in_range(res, nod, min_price, max_price, mode)]
            return models.Restaurant.objects.filter(id__in=open_restaurants_ids)

        return models.Restaurant.objects


class PopularAPI(viewsets.GenericViewSet):
    serializer_class = serializers.RestaurantSerializers

    def get_object(self):
        all_res = models.Restaurant.objects.all()
        max_amt = float(self.request.query_params.get('max_amount', '10'))
        max_res = None
        for res in all_res:
            txns = TxnModels.Transaction.objects.filter(restaurant=res)
            txn_total = sum(txn.transaction_amount for txn in txns)
            if txn_total > max_amt:
                max_amt = txn_total
                max_res = res
        return res

    def list(self, request):
        obj = self.get_object()
        data = self.serializer_class(obj).data
        return response.Response(data)
