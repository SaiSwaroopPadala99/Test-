from urllib.parse import quote, urlencode
import base64
import json
import time
import requests

# Client ID and secret
client_id = '4295589b-b5c8-4049-bofd-fda4daof21oe'
client_secret = 'rNmRikh8dR-[IE7W2[-8vx:I0R]R46:V'

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# The scopes required by the app
scopes = [ 'openid',
           'User.Read',
           'Mail.Read' ]

def get_signin_url(redirect_uri):
  # Build the query parameters for the signin url
  params = { 'client_id': client_id,
             'redirect_uri': redirect_uri,
             'response_type': 'code',
             'scope': ' '.join(str(i) for i in scopes)
            }

  signin_url = authorize_url.format(urlencode(params))

  return signin_url

  def get_token_from_code(auth_code, redirect_uri):
  # Build the post form for the token request
    post_data = { 'grant_type': 'authorization_code',
                  'code': auth_code,
                  'redirect_uri': redirect_uri,
                  'scope': ' '.join(str(i) for i in scopes),
                  'client_id': client_id,
                  'client_secret': client_secret
                }

  r = requests.post(token_url, data = post_data)

  try:
    return r.json()
  except:
    return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


    # The scopes required by the app
scopes = [ 'openid',
           'offline_access',
           'User.Read',
           'Mail.Read' ]


  def get_token_from_refresh_token(refresh_token, redirect_uri):
  # Build the post form for the token request
  post_data = { 'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(str(i) for i in scopes),
                'client_id': client_id,
                'client_secret': client_secret
              }

  r = requests.post(token_url, data = post_data)

  try:
    return r.json()
  except:
    return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


  def get_access_token(request, redirect_uri):
  current_token = request.session['access_token']
  expiration = request.session['token_expires']
  now = int(time.time())
  if (current_token and now < expiration):
    # Token still valid
    return current_token
  else:
    # Token expired
    refresh_token = request.session['refresh_token']
    new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)

    # Update session
    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + new_tokens['expires_in'] - 300

    # Save the token in the session
    request.session['access_token'] = new_tokens['access_token']
    request.session['refresh_token'] = new_tokens['refresh_token']
    request.session['token_expires'] = expiration

    return new_tokens['access_token']

  def get_my_messages(access_token):
    get_messages_url = graph_endpoint.format('/me/mailfolders/inbox/messages')

# Use OData query parameters to control the results
#  - Only first 10 results returned
#  - Only return the ReceivedDateTime, Subject, and From fields
#  - Sort the results by the ReceivedDateTime field in descending order
    query_parameters = {'$top': '10',
                        '$select': 'receivedDateTime,subject,from',
                        '$orderby': 'receivedDateTime DESC'}

    r = make_api_call('GET', get_messages_url, access_token, parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
      return r.json()
    else:
      return "{0}: {1}".format(r.status_code, r.text)