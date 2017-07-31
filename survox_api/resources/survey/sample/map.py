from ...base import SurvoxAPIBase
from ...exception import SurvoxAPIRuntime, SurvoxAPIMissingParameter, SurvoxAPINotFound


class SurvoxAPISurveySampleMap(SurvoxAPIBase):
    def __init__(self, sid=None, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveySampleMap, self).__init__(base_url, headers, verbose)
        self.sid = sid
        self.url = '/surveys/{sid}/sample/map/'.format(sid=self.sid)

    def get(self):
        return self.api_get(endpoint=self.url)

    def create(self, sample_map, exists_okay=False):
        if not sample_map:
            raise SurvoxAPIMissingParameter('sample_map')
        s = None
        try:
            s = self.get()
            if s and not exists_okay:
                raise SurvoxAPIRuntime('Sample map already exist for survey: {sid}'.format(sid=self.sid))
        except SurvoxAPINotFound:
            pass
        if not s:
            s = self.api_post(endpoint=self.url, json=sample_map)
        return s

    def set(self, sample_map):
        if not sample_map:
            raise SurvoxAPIMissingParameter('sample_map')
        return self.api_put(endpoint=self.url, json=sample_map)

    def delete(self):
        return self.api_delete(endpoint=self.url)
