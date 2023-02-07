from rest_framework import serializers
from .models import Publisher, BoardGame


class BoardGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardGame
        fields = ('id', 'name', 'min_players', 'max_players', 'publisher')


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'name')
