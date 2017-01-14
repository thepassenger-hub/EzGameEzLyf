from rest_framework.serializers import ModelSerializer
from scrape_games.models import EmailModel

class ContactSerializer(ModelSerializer):
    class Meta:
        model = EmailModel
        fields = ('name', 'email', 'subject', 'content')