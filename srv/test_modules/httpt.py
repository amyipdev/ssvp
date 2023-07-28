import requests

methods = {
    "head": requests.head,
    "get": requests.get,
    "post": requests.post
}


def http_t(srv: dict) -> bool:
    try:
        return methods[srv["args"]](srv["ip"], timeout=5, allow_redirects=True).status_code == 200
    except requests.exceptions.Timeout:
        return False
