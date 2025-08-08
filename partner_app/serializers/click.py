from rest_framework import serializers
from partner_app.models import ClickEvent

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickEvent
        fields = ["project", "partner","platform","partner_link", "partnership", "referrer","user_agent","ip_address"]