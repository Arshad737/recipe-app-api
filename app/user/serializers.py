from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
# should use this for any message to be output to the screen so that the if in future we happen to add some translation system, this can handle it 
from django.utils.translation import ugettext_lazy as _ 

class UserSerializer(serializers.ModelSerializer):
    '''Serialiser for user object '''
    class Meta: 
        model=get_user_model()
        fields=('email', 'password', 'name')
        extra_kwargs={'password': {'write_only':True, 'min_length':5}}

    def create(self, validated_data):
        '''create a new user an encypted passowrd and return it'''
        return get_user_model().objects.create_user(**validated_data)
    

class AuthTokenSerializer(serializers.Serializer):
    '''Serialiser for uiser authentication object'''
    email=serializers.CharField()
    password= serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        '''validate and authenticate user'''
        email=attrs.get('email')
        password=attrs.get('password')
        # to get request context => self.context.get('request)

        user= authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
            )

        print(user.__dir__)
            
        if not user:
            msg= _('unable to authicate with provided creds')
            raise serializers.ValidationError(msg, code='authentication ')

        attrs['user']=user
        return attrs


                        
