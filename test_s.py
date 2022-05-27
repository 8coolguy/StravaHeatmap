from stravalib.client import Client
from download_data import get_api_values
from download_data import get_strava_api
from make_heatmap import heatmap
import webbrowser
import requests

s,ids=get_api_values()
client = Client()
authorize_url=""
authorize_url = client.authorization_url(client_id=ids, redirect_uri='http://127.0.0.1:5000/')
# Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
# .....
wUrl=webbrowser.open(authorize_url)

# Extract the code from your webapp response
code = "6b45eaa4ac67e8d40e258acf7d541339ea9f235d" # or whatever your framework does
token_response = client.exchange_code_for_token(client_id=ids, client_secret=s, code=code)
access_token = token_response['access_token']
refresh_token = token_response['refresh_token']
expires_at = token_response['expires_at']

# Now store that short-lived access token somewhere (a database?)
client.access_token = access_token
# You must also store the refresh token to be used later on to obtain another valid access token
# in case the current is already expired
client.refresh_token = refresh_token

# An access_token is only valid for 6 hours, store expires_at somewhere and
# check it before making an API call.
client.token_expires_at = expires_at
athlete = client.get_athlete()
get_strava_api(client)
heatmap(client)
print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))
