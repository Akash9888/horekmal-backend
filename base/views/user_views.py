from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import User
from base.randerers import UserRenderer
from base.serializer import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer, SendPasswordResetSerializer, UserPasswordResetSerializer, GetAllUsersSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg': "Registration Successful", "token": token}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        # print(request.user)
        data = request.data
        # print(data)
        # print(data['email'])
        # serializer = UserLoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # email = serializer.data.get('email')
        # password = serializer.data.get('password')
        user = authenticate(email=data['email'], password=data['password'])

        if user is not None:
            email = data['email']
            user_info = User.objects.filter(email=email).values()
            # print(user_info)
            # # serializer2=GetAllUsersSerializer(email=email)
            # email=data['email']
            # print(email)
            # user_info = User.objects.filter(email)
            serializer = UserLoginSerializer(user_info, many=True)
            token = get_tokens_for_user(user)
            # print(serializer.data)

            user_data = serializer.data
            user_data = user_data[0]
            user_data["token"] = token

            return Response({'user': user_data}, status=status.HTTP_200_OK)

        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}},
                            status=status.HTTP_400_BAD_REQUEST)


class GetAllUsersView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = GetAllUsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': "password change successfully"}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = SendPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': "password Reset Link send. Please check your Email"}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': "password reset successfully"}, status=status.HTTP_200_OK)

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         # data['username']=self.user.username
#         # data['email']=self.user.email
#         serializer = UserSerializerwithToken(self.user).data
#
#         for key, value in serializer.items():
#             data[key] = value
#
#         return data
#
#
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
#
#
# # create user
# @api_view(['POST'])
# def registerUser(request):
#     data = request.data
#     try:
#         user = User.objects.create_user(
#             first_name=data['name'],
#             username=data['name'],
#             email=data['email'],
#             password=make_password(data['password'])
#         )
#         serializer = UserSerializerwithToken(user, many=False)
#         return Response(serializer.data)
#     except:
#         return Response({'error': 'user already exists'}, status=400)
#
#
# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def getUsers(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateUserProfile(request):
#     user = request.user
#     serializer = UserSerializer(user, many=False)
#     data = request.data
#
#     user.first_name = data['name']
#     user.username = data['email']
#     user.email = data['email']
#     if data['password'] != '':
#         user.password = make_password(data['password'])
#
#     user.save();
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getUserProfile(request):
#     user = request.user
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)
