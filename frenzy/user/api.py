from rest_framework import viewsets, mixins, response
from django_filters import rest_framework as df_filters
from datetime import datetime

from frenzy.user import models, serializers, filters


class UserAPI(
    # mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    filter_backends = [df_filters.DjangoFilterBackend]
    filterset_class = filters.UserFilter

    def get_queryset(self):
        return models.User.objects


class TransactionAPI(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        return models.Transaction.objects


class NumberOfUsersAPI(viewsets.GenericViewSet):

    def list(self, request):
        now = str(int(datetime.now().timestamp()))
        min_date = int(self.request.query_params.get('min_date', now))
        max_date = int(self.request.query_params.get('max_date', now))
        value = int(self.request.query_params.get('value', '0'))
        mode = self.request.query_params.get('mode', 'lte')

        min_date = datetime.utcfromtimestamp(min_date)
        max_date = datetime.utcfromtimestamp(max_date)

        if mode == 'gte':
            txns = models.Transaction.objects.filter(
                transaction_amount__lte=value,
                transaction_date__gte=min_date,
                transaction_date__lte=max_date,
            )
        else:
            txns = models.Transaction.objects.filter(
                transaction_amount__gte=value,
                transaction_date__gte=min_date,
                transaction_date__lte=max_date,
            )
        users = set(txn.user.id for txn in txns)

        return response.Response({'Number of user': len(users)})


class TopXUsersAPI(viewsets.GenericViewSet):
    queryset = models.User.objects

    def list(self, request):
        now = str(int(datetime.now().timestamp()))
        min_date = int(self.request.query_params.get('min_date', now))
        max_date = int(self.request.query_params.get('max_date', now))
        value = int(self.request.query_params.get('value', '10'))

        min_date = datetime.utcfromtimestamp(min_date)
        max_date = datetime.utcfromtimestamp(max_date)

        txns = models.Transaction.objects.filter(
            transaction_date__gte=min_date,
            transaction_date__lte=max_date,
        )
        amt_by_user = {}
        for txn in txns:
            if txn.user not in amt_by_user:
                amt_by_user[txn.user] = 0.0
            amt_by_user[txn.user] += txn.transaction_amount

        topx = sorted(amt_by_user.keys(), key=lambda k: amt_by_user[k])[:value]
        results = {f'{k.name}-{k.id}': amt_by_user[k] for k in topx}

        return response.Response(results)
