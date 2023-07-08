from rest_framework import serializers

class SearchFieldSerializer(serializers.Serializer):
    search = serializers.CharField()