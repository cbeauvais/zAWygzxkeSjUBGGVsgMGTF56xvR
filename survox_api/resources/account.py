from .base import SurvoxAPIBase


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

    def get(self):
        """
        Fetch details about the specified account
        :return:
        """
        for x in self.api_get(endpoint='/accounts/'):
            if x['name'] == self.name:
                return x
        return None
