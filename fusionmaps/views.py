import httplib2
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from oauth2client.contrib.django_util import decorators
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from googleapiclient.discovery import build


from .models import GeoLocation
from .models import CredentialsModel


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/plus.me',
    redirect_uri='http://localhost:8080/oauth2callback')


@login_required
def auth_return(request):
    req = request.GET
    if not xsrfutil.validate_token(
            settings.SECRET_KEY, req['state'].encode(),
            request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(req)
    storage = DjangoORMStorage(
        CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/fusionmaps")

@login_required
def index(request):
    storage = DjangoORMStorage(
        CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid is True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("fusiontables", "v2", http=http)
        table = service.table()
        import pdb; pdb.set_trace()
        table.get(tableId='1y-Bd4HBI24hMMoggv1R-1HYguga8Acq1zHVO_mwY').execute()
        logging.info(activitylist)
    addresses = GeoLocation.objects.all()
    context = {
        'addresses': addresses,
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }
    return render(request, 'index.html', context)


@login_required
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
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.request import Request

    client_id = "68093915267.apps.googleusercontent.com"
    client_secret = "hQvUSyq6AOtelQHsJscb0tVB"
    # table_id = "<table_id>"

    access_token = ""
    refresh_token = "<refresh_token>"

    #   the refresh token is used to request a new access token
    data = urlencode({
      'client_id': client_id,
      'client_secret': client_secret,
      'refresh_token': refresh_token,
      'grant_type': 'refresh_token'})
    request = Request(
      url='https://accounts.google.com/o/oauth2/token',
      data=data)
    import pdb; pdb.set_trace()
    # request_open = urlopen(request)
    # response = request_open.read()
    return JsonResponse(data)


def remove_all_addresses(request):
    GeoLocation.objects.all().delete()
    data = {'result': 'ok'}
    return JsonResponse(data)
