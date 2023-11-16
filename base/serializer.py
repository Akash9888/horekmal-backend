from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from base.Util import Util
from base.models import Product, User, ShippingAddress, OrderItem, Order
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, smart_str, DjangoUnicodeDecodeError
from django.core.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # validating Password and confirm password while registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match")
        return attrs

    def create(self, validated_data):
        print(validated_data["name"])

        del validated_data["password2"]

        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'tc', 'is_admin', 'is_active']


class GetAllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'tc', 'is_admin', 'is_active']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'tc', 'is_admin', 'is_active']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError("password and confirm password doesnt match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://loacalhost:300/api/user/reset/' + uid + '/' + token
            # email
            body = "Click following link to reset your password " + link
            data = {
                "subject": "Reset Your Password",
                "body": body,
                'to_email': user.email,

            }
            Util.send_email(data)

            return attrs
        else:
            raise ValidationError("You are not a Registered User")


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password '}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):

        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confirm password doesnt match")
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError("Token is not valid or expired")


# class UserSerializer(serializers.ModelSerializer):
#     name=serializers.SerializerMethodField(read_only=True)
#     _id=serializers.SerializerMethodField(read_only=True)
#     isAdmin=serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model=User
#         fields=['id','_id','username','email','name','isAdmin','last_login']
#
#     def get__id(self,obj):
#         return obj.id
#
#     def get_isAdmin(self,obj):
#         return obj.is_staff
#
#     def get_name(self,obj):
#         name=obj.first_name
#         if name=='':
#             name=obj.email
#         return name
#
# class UserSerializerwithToken(UserSerializer):
#     token=serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model=User
#         fields=['id','_id','username','email','name','isAdmin','last_login','token']

# def get_token(self,obj):
#     token=RefreshToken.for_user(obj)
#     return str(token.access_token)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserLoginSerializer(user, many=False)
        return serializer.data
