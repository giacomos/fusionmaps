from django.http import JsonResponse
from django.http import HttpResponseBadRequest

from django.conf import settings
from django.shortcuts import render
from .models import GeoLocation
from . import fw


def index(request):
    addresses = GeoLocation.objects.all()
    context = {
        'addresses': addresses,
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }
    return render(request, 'index.html', context)


def add_address(request):
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    address = request.GET.get('address', None)
    if (lat and lng and address):
        location = GeoLocation.create(lat, lng, address)
        addresses = GeoLocation.objects.all()
        fusion_exists = fw.address_exist(lat, lng)
        if (location in addresses or fusion_exists):
            data = {'result': 'address already added'}
            return JsonResponse(data)
        fw.add_address(address, lat, lng)
        location.save()
        print('Adding new address: %s %s %s' % (lat, lng, address))
    data = {'result': 'ok'}
    return JsonResponse(data)


def remove_all_addresses(request):
    GeoLocation.objects.all().delete()
    fw.remove_all_addresses()
    data = {'result': 'ok'}
    return JsonResponse(data)
