from survox_api.resources.base import SurvoxAPIBase

class SurvoxAPIAccountServer(SurvoxAPIBase):
    def __init__(self, account, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIAccountServer, self).__init__(base_url, headers, verbose)
        self.account = account
        self.endpoint = '/accounts/{account}/server/'.format(account=self.account)
        self.start_endpoint = '{b}start/'.format(b=self.endpoint)
        self.stop_endpoint = '{b}stop/'.format(b=self.endpoint)

    def get(self):
        """
        Return the status of the Survey server for the account
        :return:
        """
        return self.api_get(endpoint=self.endpoint)

    def start(self):
        """
        Start the Survey server for the account
        :return:
        """
        return self.api_post(endpoint=self.start_endpoint, data={})

    def stop(self, force=False):
        """
        Stops the Survey server for the account
        :param force: force the server to stop now, not recommended!
        :return:
        """
        return self.api_post(endpoint=self.endpoint, data={'force': force})
