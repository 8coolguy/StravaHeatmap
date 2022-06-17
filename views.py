from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

#all the modules for getting and plotting the data
from heatmaps.download_data import get_api_values
from heatmaps.download_data import get_strava_api
from heatmaps.make_heatmap import heatmap
from stravalib.client import Client
# Create your views here.
s,ids=get_api_values()
client = Client()
#for /heatmaps
def index(request):
    return render(request,'heatmaps/index.html')
def login(request):

    authorize_url = client.authorization_url(client_id=ids, redirect_uri='http://127.0.0.1:8000/heatmaps/map')  
    return redirect(authorize_url)
def map(request):
    code=request.GET['code']
    token_response = client.exchange_code_for_token(client_id=ids, client_secret=s, code=code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']
    client.access_token = access_token
    # You must also store the refresh token to be used later on to obtain another valid access token
    # in case the current is already expired
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at
    athlete = client.get_athlete()
    get_strava_api(client)
    heatmap(client)
    return render(request,'heatmaps/heatmap.html')
