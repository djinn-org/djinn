import httplib2
import urllib.parse
import settings


def get(path, params=''):
    # params = 'where={"room":{"__type":"Pointer","className":"Room","objectId":"%s"}}' % "Ay4Qe3A1lC"
    # body = urllib.parse.urlencode('{"where":{"room":{"__type":"Pointer","className":"Room","objectId":"{}"}}}'.format("Ay4Qe3A1lC"))

    http = httplib2.Http('.cache', 443)
    resp, content = http.request(
        'https://api.parse.com/{}'.format(path) + '?' + params,
        'GET',
        headers={
            "X-Parse-Application-Id": settings.PARSE_APP_ID,
            "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
        }
    )
    return content
