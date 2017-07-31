from ...base import SurvoxAPIBase
from ...exception import SurvoxAPIRuntime, SurvoxAPINotFound


class SurvoxAPISurveySampleCallingRules(SurvoxAPIBase):
    def __init__(self, sid=None, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveySampleCallingRules, self).__init__(base_url, headers, verbose)
        self.sid = sid
        self.url = '/surveys/{sid}/sample/calling-rules/'.format(sid=self.sid)

    def get(self):
        return self.api_get(endpoint=self.url)

    def create(self, calling_rules, exists_okay=False):
        s = None
        if not calling_rules:
            raise SurvoxAPIRuntime('missing required parameter: calling_rules')
        try:
            s = self.api_get(endpoint=self.url)
            if s and not exists_okay:
                raise SurvoxAPIRuntime('Sample calling rules already exist for survey: {sid)'.format(sid=self.sid))
        except SurvoxAPINotFound:
            pass
        if not s:
            s = self.api_post(endpoint=self.url, json=calling_rules)
        return s

    def set(self, calling_rules):
        if not calling_rules:
            raise SurvoxAPIRuntime('missing required parameter: calling_rules')
        return self.api_put(endpoint=self.url, json=calling_rules)

    def delete(self):
        return self.api_delete(endpoint=self.url)

