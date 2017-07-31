from ..exception import SurvoxAPIRuntime, SurvoxAPINotFound
from ..base import SurvoxAPIBase


class SurvoxAPISurveyQuotaList(SurvoxAPIBase):
    """
    Class to work with quota list for a survey
    """

    def __init__(self, sid, base_url=None, headers=None, verbose=True):
        if not sid:
            raise SurvoxAPIRuntime('missing required parameter: sid')
        super(SurvoxAPISurveyQuotaList, self).__init__(base_url, headers, verbose)
        self.sid = sid
        self.endpoint = '/surveys/{sid}/quotas/'.format(sid=self.sid)
        self.reset_endpoint = '/surveys/{sid}/quotas-reset/'.format(sid=self.sid)

    def list(self):
        """
        Fetch a list of survey quotas
        :return: list of quotas
        """
        return self.api_get(endpoint=self.endpoint)

    def create(self, quota_list):
        """
        Create a list of quotas, to create a single quota call 'create([quota])'.  Will only create quotas that
        don't already exist.
        :param quota_list: a list of quotas to create for the survey
        :return: the quotas created
        """
        if not quota_list:
            raise SurvoxAPIRuntime('missing required parameter: quota_list')
        if not isinstance(quota_list, list):
            raise SurvoxAPIRuntime('specified quota_list is not type list')
        current = {x['name']: 1 for x in self.list()}
        create = []
        for q in quota_list:
            if not q['name'] in current:
                create.append(q)
        if len(create):
            return self.api_post(endpoint=self.endpoint, json=create)
        return []

    def reset(self):
        """
        reset the 'current' portion of all survey quotas
        :return: not sure
        """
        return self.api_post(endpoint=self.reset_endpoint, data={})


class SurvoxAPISurveyQuota(SurvoxAPIBase):
    """
    Class to work with individual survey quotas
    """

    def __init__(self, name, sid, base_url=None, headers=None, verbose=True):
        if not name:
            raise SurvoxAPIRuntime('missing required parameter: quota name')
        super(SurvoxAPISurveyQuota, self).__init__(base_url, headers, verbose)
        self.name = name
        self.sid = sid
        self.endpoint = '/surveys/{sid}/quotas/{quota}/'.format(sid=self.sid, quota=self.name)
        self.increment_endpoint = '/surveys/{sid}/quotas/{quota}/increment/'.format(sid=self.sid, quota=self.name)

    @staticmethod
    def _qfill(q=None, current=None, total=None, target=None):

        qq = {'current': 0, 'total': 0, 'target': 0}
        if q:
            qq['current'] = q.get('current', 0)
            qq['total'] = q.get('total', 0)
            qq['target'] = q.get('target', 0)

        if current:
            qq['current'] = current
        if total:
            qq['total'] = total
        if target:
            qq['target'] = target
        return qq

    def get(self):
        """
        Fetch a specific survey quota
        :return: quota or None
        """
        try:
            return self.api_get(endpoint=self.endpoint)
        except SurvoxAPINotFound:
            return None

    def set(self, current=None, total=None, target=None, quota=None):
        """
        Set the different values for a given survey quota
        :param current: new current value of quota
        :param total: new total value of quota
        :param target: new target value of quota
        :param quota: new quota dictionary instead of individual values
        :return: updated survey quota
        """
        if not quota:
            quota = self.get()
        if not current and not total and not target and not quota:
            raise SurvoxAPIRuntime('must specify at least on component of the quota')
        q = self._qfill(quota, current, total, target)
        return self.api_put(endpoint=self.endpoint, data=q)

    def delete(self):
        """
        delete a specific survey quota
        :return: not sure
        """
        return self.api_delete(endpoint=self.endpoint)

    def increment(self, amount=None):
        """
        Increment a specific survey quota by the specified amount
        :param amount: how much to increment, may be negative
        :return: updated survey quota
        """
        if not amount:
            amount = 1
        increment = {'increment': int(amount)}
        return self.api_post(endpoint=self.increment_endpoint, data=increment)
