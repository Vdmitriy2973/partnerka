from rest_framework import serializers
from partner_app.models import Conversion

class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversion
        fields = ["project", "partner","advertiser", "amount", "details","partner_link","platform","partnership","user_agent","ip_address"]