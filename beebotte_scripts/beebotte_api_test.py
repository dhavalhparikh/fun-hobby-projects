import hmac
import json
import requests
import time
from base64 import b64encode
from datetime import datetime
from hashlib import sha1, md5
from email import utils

# Host name
hostname = "api.beebotte.com"

# All endpoints (currently only POST for write and publish is supported)
__publicReadEndpoint__  = "/v1/public/data/read"
__readEndpoint__        = "/v1/data/read"
__writeEndpoint__       = "/v1/data/write"
__publishEndpoint__     = "/v1/data/publish"
__connectionsEndpoint__ = "/v1/connections"
__channelsEndpoint__    = "/v1/channels"

# Change the following 4 variables according to your needs
API_KEY = ''
SECRET_KEY = ''
channel = "dev"
resource = "door"

# Data dict for post request
post_data = {"data": 1}

# Returns the value for the 'Authorization` key that is used to send in the http header
def create_signature(secret_key, api_key, string_to_sign):
    signature = hmac.new(secret_key.encode(), string_to_sign.encode(), sha1)
    return "%s:%s" % (api_key, bytes.decode(b64encode(signature.digest())))

# Forms the string according to https://beebotte.com/docs/auth
def sign_request(verb, uri, date, c_type, c_md5, secret_key, api_key):
    stringToSign = "%s\n%s\n%s\n%s\n%s" % (verb, c_md5, c_type, date, uri)
    return create_signature(SECRET_KEY, API_KEY, stringToSign)

# Creates the md5 of the json data sent in the POST request
def create_md5(json_data):
    md5_str = bytes.decode( b64encode( md5( str.encode( json_data ) ).digest() ) )
    # md5_str = md5(json_data.encode("utf-8")).hexdigest()
    return md5_str

# Makes the HTTP POST request
def post_request(hostname, json_data, uri):
    # Create URL
    url = "%s://%s%s" % ('https', hostname, uri)
    # get md5 and date
    md5 = create_md5(json_data)
    date = utils.formatdate()
    # get auth data
    sig = sign_request('POST', uri, date, "application/json", md5, SECRET_KEY, API_KEY)
    # create header
    headers = {'Content-Type': 'application/json', 'Content-MD5': md5, 'Date': date, "Authorization": sig}
    # make the request
    r = requests.post(url, data=json_data, headers=headers)
    print(r.status_code)
    print(r.text)

def main():
    endpoint = "%s/%s/%s" % (__writeEndpoint__, channel, resource)
    post_data['data'] = int(time.time())
    post_request(hostname, json.dumps(post_data, separators=(',',':')), endpoint)

if __name__ == "__main__":
    main()