from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from knox import views as knox_views

from . import models
from . import serializers

# Create your views here.
class JoinCourse(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        if 'course_id' not in kwargs:
            return Response({"errors": ["course_id not set in request."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course_join_code = models.CourseJoinCode.get(
                code=kwargs['course_id'])
        except:
            return Response({"errors": [f"course join code {str(kwargs['course_id'])} doesn't exist"]}, status=status.HTTP_404_NOT_FOUND)

        try:
            course_subscription = models.UserCourseSubscription(
                user=self.request.user, course=course_join_code.course)
            course_subscription.save()
        except Exception as e:
            return Response({"errors": [str(e)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)


class RegistrationView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmailPasswordLogin(knox_views.LoginView):
    """View used to login using email and password."""
    permission_classes = (AllowAny,)
    serializer_class = serializers.EmailPasswordLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response(super().post(request, format=None).data, status=status.HTTP_200_OK)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
