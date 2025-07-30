from rest_framework import serializers
from partner_app.models import Conversion

class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversion
        fields = ["project", "partner", "order_id", "amount", "meta"]