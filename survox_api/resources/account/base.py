from survox_api.resources.base import SurvoxAPIBase
from survox_api.resources.account.server import SurvoxAPIAccountServer
from survox_api.resources.valid import valid_url_field
from survox_api.resources.exception import SurvoxAPIRuntime


class SurvoxAPIAccountList(SurvoxAPIBase):
    """
    Class to manage a list of Survox accounts
    """

    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIAccountList, self).__init__(base_url, headers, verbose)

    def list(self):
        """
        Fetch a list of the survox runtime accounts
        :return:  list of accounts
        """
        return self.api_get(endpoint='/accounts/')


class SurvoxAPIAccount(SurvoxAPIBase):
    def __init__(self, name, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIAccount, self).__init__(base_url, headers, verbose)
        self.name = name
        valid, msg = valid_url_field('Account name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)

    def get(self):
        """
        Fetch details about the specified account
        :return:
        """
        for x in self.api_get(endpoint='/accounts/'):
            if x['name'] == self.name:
                return x
        return None

    @property
    def server(self):
        return SurvoxAPIAccountServer(account=self.name, base_url=self.base_url, headers=self.auth_headers,
                                        verbose=self.verbose)

