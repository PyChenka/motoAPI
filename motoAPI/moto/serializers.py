import datetime
import webcolors

from rest_framework import serializers

from .models import Bike, Owner, Ownership


class OwnerSerializer(serializers.ModelSerializer):
    current_bikes = serializers.StringRelatedField(many=True, read_only=True)
    previous_bikes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('name', 'surname', 'current_bikes', 'previous_bikes', )


class Hex2NameColor(serializers.Field):
    """Кастомный тип поля для сериализатора BikeSerializer"""

    def to_representation(self, value):
        """При чтении отображает название цвета как есть"""

        return value

    def to_internal_value(self, data):
        """При записи конвертирует код цвета в название"""

        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени.')
        return data


class MethodFieldMixin:
    def get_age(self, obj):
        """Для MethodField: вычисляет значение для поля age"""

        return datetime.datetime.now().year - obj.made_year


class BikeChangeSerializer(serializers.ModelSerializer, MethodFieldMixin):
    nickname = serializers.CharField(source='name')
    current_owner = OwnerSerializer()
    previous_owners = OwnerSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    color = Hex2NameColor()

    class Meta:
        model = Bike
        fields = ('nickname', 'brand', 'model', 'color', 'made_year', 'age', 'current_owner', 'previous_owners',)

    def create(self, validated_data):
        if 'previous_owners' not in self.initial_data:
            return self.create_bike_and_current_owner(validated_data)
        else:
            previous_owners = validated_data.pop('previous_owners')
            bike = self.create_bike_and_current_owner(validated_data)
            for owner in previous_owners:
                own, status = Owner.objects.get_or_create(**owner)
                Ownership.objects.create(owner=own, bike=bike)
            return bike

    def update(self, instance, validated_data):
        if 'previous_owners' not in self.initial_data:
            return self.update_bike_with_current_owner_create(instance, validated_data)
        else:
            previous_owners = validated_data.pop('previous_owners')
            bike = self.update_bike_with_current_owner_create(instance, validated_data)
            for owner in previous_owners:
                own, status = Owner.objects.get_or_create(**owner)
                Ownership.objects.get_or_create(owner=own, bike=bike)
            return instance

    def create_bike_and_current_owner(self, data) -> Bike:
        """Создает owner'а, если его нет, и создает bike с этим owner'ом"""

        current_owner = data.pop('current_owner')
        owner, status = Owner.objects.get_or_create(**current_owner)
        data['current_owner'] = owner
        bike = Bike.objects.create(**data)
        return bike

    def update_bike_with_current_owner_create(self, instance, data) -> Bike:
        """Создает owner'а, если его нет, и обновляет bike"""

        current_owner = data.pop('current_owner')
        owner, status = Owner.objects.get_or_create(**current_owner)
        instance.current_owner = owner
        instance.name = data.get('name', instance.name)
        instance.brand = data.get('brand', instance.brand)
        instance.model = data.get('model', instance.model)
        instance.color = data.get('color', instance.color)
        instance.made_year = data.get('made_year', instance.made_year)
        instance.save()
        return instance


class OwnerRelatedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = ('full_name', )

    def get_full_name(self, obj):
        """Для MethodField: слепляет полное имя для поля full_name"""

        return f'{obj.name} {obj.surname}'


class BikeListSerializer(serializers.ModelSerializer, MethodFieldMixin):
    nickname = serializers.CharField(source='name')
    color = Hex2NameColor()
    current_owner = OwnerRelatedSerializer()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Bike
        fields = ('nickname', 'brand', 'model', 'color', 'made_year', 'age', 'current_owner', )


class BikeDetailSerializer(serializers.ModelSerializer, MethodFieldMixin):
    nickname = serializers.CharField(source='name')
    current_owner = OwnerRelatedSerializer()
    previous_owners = OwnerRelatedSerializer(many=True)
    color = Hex2NameColor()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Bike
        fields = ('nickname', 'brand', 'model', 'color', 'made_year', 'age', 'current_owner', 'previous_owners', )



