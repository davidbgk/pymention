import json

from checkers import errors


def bad_method(start_response):
    """Returns a 405 in case the HTTP method is not POST.

    TODO: better returning a form to manually submit a relation?
    """
    data = "Only POST method is allowed. See http://webmention.org/"
    start_response("405 Method not allowed", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])


def bad_request(start_response, accept_header, error_message):
    """Returns a 400 in case an error occured related to parameters."""
    if accept_header in ('application/json', '*/*'):
        json_dict = {
            "error": error_message,
            "error_description": errors[error_message]
        }
        data = json.dumps(json_dict)
        content_type = "application/json"
    else:
        data = """<!DOCTYPE html>
        <html lang="en">
          <head>
            <title>WebMention</title>
          </head>
          <body>
            <h2>{error}</h2>
            <p>{error_description}</p>
          </body>
        </html>""".format(
            error=error_message,
            error_description=errors[error_message]
        )
        content_type = "text/html"
    start_response("400 Bad Request", [
        ("Content-Type", content_type),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])


def post_response(start_response, accept_header, post_data):
    """Returns a successful message (accepted headers are JSON or HTML)."""
    if accept_header in ('application/json', '*/*'):
        data = '{"result": "WebMention was successful"}'
        start_response("202 Accepted", [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(data)))
        ])
    elif accept_header in ('text/html',):
        data = """<!DOCTYPE html>
        <html lang="en">
          <head>
            <title>WebMention</title>
          </head>
          <body>
            <p>
              <a href="http://webmention.org/">WebMention</a> was successful.
            </p>
          </body>
        </html>"""
        start_response("202 Accepted", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
    else:
        data = ("Wrong Accept header. We can provide only text/html or"
                " application/json. See http://webmention.org/\n"
                "Accept header is %s" % accept_header)
        start_response("406 Not acceptable", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(data)))
        ])
    return iter([data])
