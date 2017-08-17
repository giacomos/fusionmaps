from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import GeoLocation


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        addresses = GeoLocation.objects.all()
        context = {
            'some_dynamic_value': 'This text comes from django view!',
            'addresses': addresses
        }
        return self.render_to_response(context)


def add_address(request):
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    address = request.GET.get('address', None)
    if (lat and lng and address):
        location = GeoLocation.create(lat, lng, address)
        addresses = GeoLocation.objects.all()
        if (location in addresses):
            data = {'result': 'address already added'}
            return JsonResponse(data)
        location.save()
        print('Adding new address: %s %s %s' % (lat, lng, address))
    data = {'result': 'ok'}
    return JsonResponse(data)


def remove_all_addresses(request):
    GeoLocation.objects.all().delete()
    data = {'result': 'ok'}
    return JsonResponse(data)
