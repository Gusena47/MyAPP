import time
from datetime import datetime


from django.http import HttpRequest
from django.shortcuts import render

from Project47 import settings


def set_useragent_on_request_middlwere(get_response):

    def middleware(request: HttpRequest):
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)

        return response

    return middleware


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_time = 0
        self.ip_time = {}
        self.time = 0
        self.rate_ms = settings.THROTTLING_RATE_MS
        self.time_req = 5
    #
    # @classmethod
    # def get_client_ip(cls, request: HttpRequest):
    #     ip = request.META.get('REMOTE_ADDR')  # Get client IP address
    #     return ip
    #
    # def request_is_allowed(self, client_ip: str) -> bool:
    #     self.now = datetime.now()
    #     self.bucket[client_ip] = self.now
#
    def __call__(self, request: HttpRequest):
        if request.META.get('REMOTE_ADDR') not in self.ip_time:
            self.ip_time[request.META.get('REMOTE_ADDR')] = time.time()
            print(self.ip_time)
        elif time.time() - self.ip_time[request.META.get('REMOTE_ADDR')] <= self.time_req:
            return render(request, 'shopppCat/erorr_req.html')
            self.ip_time[request.META.get('REMOTE_ADDR')] = time.time()
            print(self.ip_time)
        else:
            self.ip_time[request.META.get('REMOTE_ADDR')] = time.time()
            print(self.ip_time)

        response = self.get_response(request)
        return response
