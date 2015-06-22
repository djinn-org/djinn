import httplib2
import urllib.parse
import settings


def get(path, where=None):
    if where:
        body = urllib.parse.urlencode({'where': where})
    else:
        body = {}

    http = httplib2.Http('api.parse.com', 443)
    resp, content = http.request(
        'https://api.parse.com/{}'.format(path),
        'GET',
        headers={
            "X-Parse-Application-Id": settings.PARSE_APP_ID,
            "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
        },
        body=body
    )
    return content
