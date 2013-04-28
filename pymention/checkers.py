import requests

from storage import retrieve_relation, is_valid_target

# Standard errors except the `invalid_data` one.
errors = {
    "invalid_data": "The source and target parameters do not exist.",
    "source_not_found": "The source URI does not exist.",
    "target_not_found": "The target URI does not exist.",
    "target_not_supported": ("The specified target URI is not a "
                             "WebMention-enabled resource."),
    "no_link_found": ("The source URI does not contain a link"
                      " to the target URI."),
    "already_registered": ("The specified WebMention has already been"
                           " registered."),
}


def is_valid_url(url):
    """Checks the validity of a URL."""
    if not url.startswith('http'):
        return False

    try:
        response = requests.head(url)
    except requests.ConnectionError:
        return False
    return response.status_code == 200


def is_invalid_data(data):
    """Checks the validity of the `source` and `target`."""
    if not (data.keys() == ['source', 'target']
            and data.get('source') and data.get('target')):
        return "invalid_data"

    source = data['source'][0]
    target = data['target'][0]

    if not is_valid_url(source):
        return "source_not_found"

    if not is_valid_url(target):
        return "target_not_found"

    if not is_valid_target(target):
        return "target_not_supported"

    if retrieve_relation(source, target) is not None:
        return "already_registered"

    return False
