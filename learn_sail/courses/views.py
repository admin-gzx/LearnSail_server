from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


