from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role')


class UserMeSerializers(UserSerializer):
    def get_fields(self):
        fields = super(UserMeSerializers, self).get_fields()
        if self.instance and getattr(self.instance, 'role') == 'user':
            fields['role'].read_only = True
        return fields