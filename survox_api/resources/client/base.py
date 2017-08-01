from survox_api.resources.base import SurvoxAPIBase
from survox_api.resources.exception import SurvoxAPIRuntime, \
    SurvoxAPIMissingParameter, SurvoxAPINotFound
from survox_api.resources.valid import valid_url_field
from survox_api.resources.client.credentials import SurvoxAPIClientCredentialList, \
    SurvoxAPIClientCredential


class SurvoxAPIClientList(SurvoxAPIBase):
    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIClientList, self).__init__(base_url, headers, verbose)
        self.url = '/clients/'

    def list(self):
        return self.api_get(endpoint=self.url)

    def create(self, name, client_description, exists_okay=False):
        valid, msg = valid_url_field('Client name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        try:
            s = self.api_get(endpoint='{base}{client}/'.format(base=self.url, client=name))
            if not exists_okay:
                raise SurvoxAPIRuntime('Client already exists: {client)'.format(client=name))
            return s
        except SurvoxAPINotFound:
            pass
        s = self.api_post(endpoint=self.url, data={
            'client': name,
            'name': client_description
        })
        return s


class SurvoxAPIClient(SurvoxAPIBase):
    def __init__(self, name, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIClient, self).__init__(base_url, headers, verbose)
        self.name = name
        self.url = '/clients/{client}/'.format(client=self.name)

    def get(self):
        try:
            return self.api_get(endpoint=self.url)
        except SurvoxAPINotFound:
            return None

    def set(self, client):
        """
        update a client entry
        :param client: client dictionary
        :return: return the DNC list properties
        """
        if not client:
            raise SurvoxAPIMissingParameter('client')
        c = self.get()
        if not c:
            raise SurvoxAPIRuntime('No client available named: {name}'.format(name=self.name))
        return self.api_put(endpoint=self.url, data=client)

    def delete(self):
        return self.api_delete(endpoint=self.url)

    @property
    def credentials(self):
        return SurvoxAPIClientCredentialList(client=self.name, base_url=self.base_url, headers=self.auth_headers,
                                             verbose=self.verbose)

    # @property
    # def quotas(self):
    #     self._get_required()
    #     return SurvoxAPISurveyQuotaList(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
    #                                     verbose=self.verbose)
    #
    def credential(self, third_party):
        return SurvoxAPIClientCredential(third_party=third_party, client=self.name, base_url=self.base_url,
                                         headers=self.auth_headers,
                                         verbose=self.verbose)

    def get_credentials(self):
        return self.api_get(endpoint='{base}credentials/'.format(base=self.url))

    def add_credentials(self, data):
        return self.api_post(endpoint='{base}credentials/'.format(base=self.url), data=data)

    def get_credentials_third_party(self, third_party):
        return self.api_get(
            endpoint='{base}credentials/{third_party}/'.format(base=self.url, third_party=third_party))

    def delete_credentials_third_party(self, third_party):
        return self.api_delete(
            endpoint='{base}credentials/{third_party}/'.format(base=self.url, third_party=third_party))
