from rest_framework import serializers

from .models import Bike, Owner, Ownership


class OwnerSerializer(serializers.ModelSerializer):
    current_bikes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('name', 'surname', 'current_bikes', 'previous_bikes', )


class BikeSerializer(serializers.ModelSerializer):
    # current_owner = serializers.StringRelatedField(read_only=True)
    previous_owners = OwnerSerializer(many=True, required=False)

    class Meta:
        model = Bike
        fields = ('name', 'brand', 'model', 'color', 'made_year', 'current_owner', 'previous_owners',)

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
