import json

import httplib2
import settings

connection = httplib2.Http('api.parse.com', 443)
resp, content = connection.request(
    'https://api.parse.com/1/classes/Host',
    'GET',
    headers={
        "X-Parse-Application-Id": settings.PARSE_APP_ID,
        "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
    }
)
print(json.dumps(json.loads(content.decode()), indent=4))
