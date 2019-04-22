# helper/url_defender.py

from urllib.parse import urlparse, urljoin
from flask import request, url_for

def is_safe_url(target_url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target_url))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
