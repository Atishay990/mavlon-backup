from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    Name = serializers.CharField(max_length=200)


class LeadSerializer(serializers.Serializer):
    FirstName = serializers.CharField(max_length=200)
    LastName = serializers.CharField(max_length=200)
    Company = serializers.CharField(max_length=200)

class EmailSerializer(serializers.Serializer):
    Subject = serializers.CharField(max_length=200)
    TextBody = serializers.CharField(max_length=200)
    fromEmail = serializers.CharField(max_length=200)
    Incoming = serializers.BooleanField()
    Status = serializers.IntegerField()
    ToIds = serializers.ListField(
    child=serializers.CharField(max_length=100)
   )

