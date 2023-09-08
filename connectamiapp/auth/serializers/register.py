from rest_framework import serializers

from connectamiapp.user.serializers import UserSerializer
from connectamiapp.user.models import User


class RegisterSerializer(UserSerializer):
    """
   Registration serializer for user creation.

   Inherits from UserSerializer.

   Attributes:
       password (serializers.CharField): User's password (8-128 characters, write-only).

   Meta:
       model (User): User model.
       fields (list of str): Fields for request/response (id, bio, avatar, email, username, first_name, last_name, password).
   """
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        # List of all the fields that can be included in a request or a response
        fields = ['id', 'bio', 'avatar', 'email', 'username',
                  'first_name', 'last_name', 'password']


def create(self, validated_data):
    """
    Create a new user.

    Args:
        validated_data (dict): Validated data for user creation.

    Returns:
        User: Newly created User instance.
    """
    return User.objects.create_user(**validated_data)
