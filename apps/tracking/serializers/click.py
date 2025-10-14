from rest_framework import serializers
from apps.tracking.models import ClickEvent

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickEvent
        fields = ["project", "partner","advertiser","platform","partner_link", "partnership", "user_agent","ip_address","referrer"]