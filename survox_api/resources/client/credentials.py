from survox_api.resources.base import SurvoxAPIBase
from survox_api.resources.exception import SurvoxAPIRuntime, \
    SurvoxAPIMissingParameter, SurvoxAPINotFound
from survox_api.resources.valid import valid_url_field


class SurvoxAPIClientCredentialList(SurvoxAPIBase):
    def __init__(self, client, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIClientCredentialList, self).__init__(base_url, headers, verbose)
        self.client = client
        self.url = '/clients/{client}/credentials/'.format(client=self.client)

    def list(self):
        return self.api_get(endpoint=self.url)

    def create(self, third_party, credentials, exists_okay=False):
        valid, msg = valid_url_field('Client name', third_party, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        try:
            s = self.api_get(endpoint='{base}{third_party}/'.format(base=self.url, third_party=third_party))
            if not exists_okay:
                raise SurvoxAPIRuntime('Credentials already exist for: {third_party)'.format(third_party=third_party))
            return s
        except SurvoxAPINotFound:
            pass
        s = self.api_post(endpoint=self.url, data={
            'third_party': third_party,
            'credentials': credentials
        })
        return s


class SurvoxAPIClientCredential(SurvoxAPIBase):
    def __init__(self, third_party, client, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIClientCredential, self).__init__(base_url, headers, verbose)
        self.client = client
        self.third_party = third_party
        self.url = '/clients/{client}/credentials/{third_party}/'.format(client=client, third_party=third_party)

    def get(self):
        try:
            return self.api_get(endpoint=self.url)
        except SurvoxAPINotFound:
            return None

    def set(self, credentials):
        """
        update a client credentials entry
        :param credentials: third-party credentials as a json string
        :return: return updated json string of the clients third-party credentials
        """
        if not credentials:
            raise SurvoxAPIMissingParameter('client')
        c = self.get()
        if not c:
            raise SurvoxAPIRuntime(
                'No client credential available named: {third_party}'.format(third_party=self.third_party))
        return self.api_put(endpoint=self.url, data=credentials)

    def delete(self):
        return self.api_delete(endpoint=self.url)

        # def get_credentials(self):
        #     return self.api_get(endpoint='{base}credentials/'.format(base=self.url))
        #
        # def add_credentials(self, data):
        #     return self.api_post(endpoint='{base}credentials/'.format(base=self.url), data=data)
        #
        # def get_credentials_third_party(self, third_party):
        #     return self.api_get(
        #         endpoint='{base}credentials/{third_party}/'.format(base=self.url, third_party=third_party))
        #
        # def delete_credentials_third_party(self, third_party):
        #     return self.api_delete(
        #         endpoint='{base}credentials/{third_party}/'.format(base=self.url, third_party=third_party))
