from rest_framework import serializers
from api.models import EmailRequest


class EmailRequestSerializer(serializers.ModelSerializer):
    sender = serializers.EmailField()
    to = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super(EmailRequestSerializer, self).__init__(*args, **kwargs)
        self.fields['from'] = self.fields['sender']
        del self.fields['sender']

    class Meta:
        model = EmailRequest
        fields = '__all__'

