from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import CommonPasswordValidator
from rest_framework.permissions import IsAdminUser
from django.contrib import messages
import difflib

from .serializers import UserSerializer
from rest_framework import generics


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get("token", "")
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get("token", "")
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get("token", "")
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get("username", "")
        pwd = request.data.get("password", "")
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({"user_pk": user.pk, "token": token.key}, HTTP_201_CREATED)


class UserList(APIView):
    permission_classes = [IsAdminUser]  # Restringir acceso a usuarios admin

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterUserView(APIView):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        username = request.data.get("username", "")
        pwd = request.data.get("password", "")
        email = request.data.get("email", "")
        confirm_email = request.data.get("email_conf", "")
        confirm_pwd = request.data.get("password_conf", "")
        if not username or not pwd or not email or not confirm_pwd or not confirm_email:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        error_messages = []

        if User.objects.filter(username=username).exists():
            error_messages.append(
                "Username already exists. Please choose a different username."
            )

        if len(pwd) < 8:
            error_messages.append("Password must contain at least 8 characters.")

        if pwd.isdigit():
            error_messages.append(
                "Password cannot be entirely numeric. Please include alphabetic or special characters."
            )

        if pwd != confirm_pwd:
            error_messages.append("Passwords do not match. Please try again.")

        if email != confirm_email:
            error_messages.append("Emails do not match. Please try again.")

        try:
            validator = CommonPasswordValidator()
            validator.validate(pwd)
        except ValidationError:
            error_messages.append(
                "Password is commonly used. Please choose a different password."
            )

        matcher = difflib.SequenceMatcher(a=username.lower(), b=pwd.lower())
        if matcher.ratio() > 0.7:
            error_messages.append(
                "Password cannot be similar to the username. Please choose a different password."
            )

        if error_messages:
            return render(request, "register.html", {"error_messages": error_messages})
        try:

            user = User(username=username, email=email)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        messages.success(request, "User created successfully")
        return redirect("home")

class LoginUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"message": "Ya has iniciado sesión."}, status=HTTP_200_OK)
        return render(request, "login.html")

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        if not username or not password:
            return Response({"message": "Por favor, proporciona tanto el nombre de usuario como la contraseña."}, status=HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login done successfully")
            return redirect("home")
        else:
            return Response({"message": "Nombre de usuario o contraseña incorrectos."}, status=HTTP_400_BAD_REQUEST)
