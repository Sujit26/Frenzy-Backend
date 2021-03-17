from rest_framework import serializers

from frenzy.restaurant import models


class RestaurantSerializers(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()
    opening_time = serializers.SerializerMethodField()

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     seedr_folder_id = validated_data['seedr_folder_id']
    #     tmdb_id = validated_data['tmdb_id']
    #     return models.update_or_create_history(user, tmdb_id, seedr_folder_id)
    def get_menu(self, obj):
        qs = models.FoodItem.objects.filter(restaurant=obj)
        return FoodSerializer(qs, many=True).data

    def get_opening_time(self, obj):
        qs = models.OpenningTime.objects.filter(restaurant=obj)
        return OpeningTimeSerializer(qs, many=True).data

    class Meta:
        model = models.Restaurant
        fields = ['cash_balance', 'name', 'menu', 'opening_time']


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FoodItem
        fields = ['name', 'price']


class OpeningTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OpenningTime
        fields = ['weekday', 'from_hour', 'to_hour']
