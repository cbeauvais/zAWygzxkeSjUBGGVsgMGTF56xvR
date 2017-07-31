from ...base import SurvoxAPIBase
from ...exception import SurvoxAPIRuntime, SurvoxAPINotFound


class SurvoxAPISurveySampleSetupRules(SurvoxAPIBase):
    def __init__(self, sid=None, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveySampleSetupRules, self).__init__(base_url, headers, verbose)
        self.sid = sid
        self.url = '/surveys/{sid}/sample/setup-rules/'.format(sid=self.sid)

    def get(self):
        return self.api_get(endpoint=self.url)

    def create(self, setup_rules, exists_okay=False):
        if not setup_rules:
            raise SurvoxAPIRuntime('missing required parameter: setup_rules')
        s = None
        try:
            s = self.api_get(endpoint=self.url)
            if s and not exists_okay:
                raise SurvoxAPIRuntime('Sample setup rules already exist for survey: {sid)'.format(sid=self.sid))
        except SurvoxAPINotFound:
            pass
        if not s:
            s = self.api_post(endpoint=self.url, json=setup_rules)
        return s

    def set(self, setup_rules):
        if not setup_rules:
            raise SurvoxAPIRuntime('missing required parameter: setup_rules')
        return self.api_put(endpoint=self.url, json=setup_rules)

    def delete(self):
        return self.api_delete(endpoint=self.url)

