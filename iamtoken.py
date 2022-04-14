import requests


def gettoken(oauthtoken):
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    params = {
        'yandexPassportOauthToken': oauthtoken,
    }
    with requests.post(url, params=params) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
        return resp.json()["iamToken"]
