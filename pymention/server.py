from urlparse import parse_qs

from checkers import is_invalid_data
from views import bad_method, post_response, bad_request


def app(environ, start_response):
    """Dispatches the request given the method, headers and parameters."""
    method = environ.get('REQUEST_METHOD', 'GET')
    if method == 'POST':
        accept_header = environ.get('HTTP_ACCEPT', '*/*')
        body = ''
        try:
            length = int(environ.get('CONTENT_LENGTH', '0'))
        except ValueError:
            length = 0
        if length != 0:
            body = environ['wsgi.input'].read(length)
        post_data = parse_qs(body.decode())
        error = is_invalid_data(post_data)
        if not body or error:
            return bad_request(start_response, accept_header, error)
        return post_response(start_response, accept_header, post_data)
    else:
        return bad_method(start_response)
