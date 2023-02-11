import datetime
import webcolors

from rest_framework import serializers

from .models import Bike, Owner, Ownership


class OwnerSerializer(serializers.ModelSerializer):
    current_bikes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('name', 'surname', 'current_bikes', 'previous_bikes', )


class Hex2NameColor(serializers.Field):
    """Кастомный тип поля для сериализатора BikeSerializer"""

    def to_representation(self, value):
        """При чтении отображает название цвета как есть"""
        return value

    def to_internal_value(self, data):
        """При записи конверитирует код цвета в название"""
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени.')
        return data


class BikeSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='name')
    previous_owners = OwnerSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    color = Hex2NameColor()

    class Meta:
        model = Bike
        fields = ('nickname', 'brand', 'model', 'color', 'made_year', 'age', 'current_owner', 'previous_owners',)

    def create(self, validated_data):
        if 'previous_owners' not in self.initial_data:
            bike = Bike.objects.create(**validated_data)
            return bike
        else:
            previous_owners = validated_data.pop('previous_owners')
            bike = Bike.objects.create(**validated_data)
            for owner in previous_owners:
                own, status = Owner.objects.get_or_create(**owner)
                Ownership.objects.create(owner=own, bike=bike)
            return bike

    def update(self, instance, validated_data):
        if 'previous_owners' not in self.initial_data:
            instance.name = validated_data.get('name', instance.name)
            instance.brand = validated_data.get('brand', instance.brand)
            instance.model = validated_data.get('model', instance.model)
            instance.color = validated_data.get('color', instance.color)
            instance.made_year = validated_data.get('made_year', instance.made_year)
            instance.current_owner = validated_data.get('current_owner', instance.current_owner)
            instance.save()
            return instance
        else:
            previous_owners = validated_data.pop('previous_owners')
            for owner in previous_owners:
                own, status = Owner.objects.get_or_create(**owner)
                Ownership.objects.create(owner=own, bike=instance)
            return instance

    def get_age(self, obj):
        return datetime.datetime.now().year - obj.made_year
