from rest_framework import serializers
from datetime import datetime

from frenzy.user import models


class UserSerializer(serializers.ModelSerializer):
    purchase_history = serializers.SerializerMethodField()

    def get_purchase_history(self, obj):
        qs = models.Transaction.objects.filter(user=obj)
        return TransactionSerializer(qs, many=True).data

    class Meta:
        model = models.User
        fields = ['cash_balance', 'id', 'name', 'purchase_history']


class TransactionSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['user'].cash_balance < data['dish_name'].price:
            raise serializers.ValidationError("Not enough money")
        return data

    def create(self, validated_data):
        validated_data['transaction_amount'] = validated_data['dish_name'].price
        validated_data['transaction_date'] = datetime.now()

        user = validated_data['user']
        user.cash_balance -= validated_data['transaction_amount']

        res = validated_data['dish_name'].restaurant
        res.cash_balance += validated_data['transaction_amount']
        validated_data['restaurant'] = res

        txn = models.Transaction.objects.create(**validated_data)

        user.save()
        txn.save()
        res.save()

        return txn

    class Meta:
        model = models.Transaction
        fields = "__all__"
        read_only_fields = [
            'restaurant',
            'transaction_amount',
            'transaction_date'
        ]
