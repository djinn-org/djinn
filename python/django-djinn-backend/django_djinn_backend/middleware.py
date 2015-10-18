import logging


class RequestLogMiddleware(object):

    def __init__(self):
        self.logger = logging.getLogger('requests')

    def process_response(self, request, response):
        self.logger.info('{} {} {} {} {}'.format(
            request.META['REMOTE_ADDR'], request.method, request.get_full_path(),
            response.status_code, len(response.content))
        )

        return response
