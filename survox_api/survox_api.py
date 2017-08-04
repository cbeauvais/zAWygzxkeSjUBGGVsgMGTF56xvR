import requests
from urllib.parse import urlparse

from .resources.valid import valid_url_field
from .resources.base import SurvoxAPIBase
from .resources.account.base import SurvoxAPIAccountList, SurvoxAPIAccount
from .resources.client.base import SurvoxAPIClientList, SurvoxAPIClient
from .resources.exception import SurvoxAPIRuntime
from .resources.survey.base import SurvoxAPISurveyList, SurvoxAPISurvey
from .resources.library.base import SurvoxAPILibrary
from .resources.exception import SurvoxAPIException


class SurvoxAPI:
    api_version = 'v0'

    def __init__(self, host=None, api_key=None, username=None, password=None, verbose=True):

        if not host:
            raise SurvoxAPIRuntime('Parameter "host" is required')

        self.host = host
        self.base_url = self._host_to_base_url()
        self.verbose = verbose
        self.oauth2_token = None
        self.headers = None
        if api_key:
            self.set_authorization_header('ApiKey', api_key)
        elif username and password:
            self.login(username=username, password=password)
        else:
            raise SurvoxAPIRuntime('Missing authentication credentials.  Must provide api_key or username/password')

    def _host_to_base_url(self):
        host = self.host
        uri = urlparse(host)
        if not uri.scheme:
            uri = urlparse('http://' + host)
            host = uri.geturl()
        allowed_schemes = ['http', 'https']
        if uri.scheme not in allowed_schemes:
            raise SurvoxAPIRuntime('Bad scheme "{s}" - must be {a}'.format(s=uri.scheme, a=', '.join(allowed_schemes)))

        if not uri.path:
            uri = urlparse('{h}/survoxapi/{v}'.format(h=host, v=self.api_version))

        if not uri.netloc or not uri.path:
            raise SurvoxAPIRuntime('Bad host "{h}" - use https://www.host.com'.format(h=host))
        if uri.username or uri.password:
            raise SurvoxAPIRuntime('Bad host "{h}" - use https://www.host.com'.format(h=host))
        if uri.params or uri.query or uri.fragment:
            raise SurvoxAPIRuntime('Bad host "{h}" - cannot contain parameters or query string'.format(h=host))

        url = uri.geturl()
        if url.endswith('/'):
            url = url[:-1]
        return url

    def set_authorization_header(self, token_type, token_value):
        self.headers = {'Authorization': '{type} {value}'.format(type=token_type, value=token_value)}

    def clear_authorization_header(self):
        self.headers = {'X-Disguised-Authorization': 'TokenType no-token-to-send'}
        self.oauth2_token = None

    def login(self, username=None, password=None, refresh_token=None):
        self.clear_authorization_header()

        login_url = "{}/auth/login/".format(self.base_url)
        if username and password:
            response = requests.post(url=login_url, data={'username': username, 'password': password})
        elif refresh_token:
            response = requests.post(url=login_url, data={'refresh_token': refresh_token})
        else:
            raise SurvoxAPIRuntime("Missing login credentials")

        try:
            if 'data' in response.json() and 'token' in response.json()['data']:
                self.oauth2_token = response.json()['data']['token']
                if 'access_token' in self.oauth2_token:
                    if 'refresh_token' not in self.oauth2_token:
                        raise SurvoxAPIRuntime(
                            'Error[{code}] - {method} {url} - {text}'.format(code='Login Failed', method='POST',
                                                                             url=login_url, text=response.text))
                    self.set_authorization_header('Bearer', self.oauth2_token['access_token'])
        except ValueError:
            self.oauth2_token = None
        return response

    def get(self, endpoint):
        api = SurvoxAPIBase(base_url=self.base_url, headers=self.headers, verbose=self.verbose)
        return api.api_get(endpoint=endpoint)

    def post(self, endpoint, data=None, json=None):
        api = SurvoxAPIBase(base_url=self.base_url, headers=self.headers, verbose=self.verbose)
        return api.api_post(endpoint=endpoint, data=data, json=json)

    def put(self, endpoint, data=None, json=None):
        api = SurvoxAPIBase(base_url=self.base_url, headers=self.headers, verbose=self.verbose)
        return api.api_put(endpoint=endpoint, data=data, json=json)

    def delete(self, endpoint):
        api = SurvoxAPIBase(base_url=self.base_url, headers=self.headers, verbose=self.verbose)
        return api.api_delete(endpoint=endpoint)

    def health(self):
        return self.status()

    def swagger(self):
        api = SurvoxAPIBase(base_url=self.base_url, headers=self.headers, verbose=self.verbose)
        r = api.api_get(endpoint='/swagger/', full_response=True)
        if r.status_code != 200:
            raise SurvoxAPIException('GET', '/swagger/', r)
        return r.json()

    def status(self):
        api = SurvoxAPIBase(base_url=self.base_url, headers=self.headers, verbose=self.verbose)
        return api.api_get(endpoint='/status/')

    @property
    def accounts(self):
        return SurvoxAPIAccountList(base_url=self.base_url, headers=self.headers, verbose=self.verbose)

    def account(self, name):
        valid, msg = valid_url_field('Account name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPIAccount(name, base_url=self.base_url, headers=self.headers, verbose=self.verbose)

    @property
    def clients(self):
        return SurvoxAPIClientList(base_url=self.base_url, headers=self.headers, verbose=self.verbose)

    def client(self, name):
        valid, msg = valid_url_field('Client name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPIClient(name, base_url=self.base_url, headers=self.headers, verbose=self.verbose)

    @property
    def surveys(self):
        return SurvoxAPISurveyList(base_url=self.base_url, headers=self.headers, verbose=self.verbose)

    def survey(self, sid):
        valid, msg = valid_url_field('Survey surveycode', sid, 1, 28)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPISurvey(sid=sid, base_url=self.base_url, headers=self.headers, verbose=self.verbose)

    @property
    def library(self):
        return SurvoxAPILibrary(base_url=self.base_url, headers=self.headers, verbose=self.verbose)
