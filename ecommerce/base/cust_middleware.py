from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from base import methods


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('middleware')

    def process_response(self, request, response):
        return response