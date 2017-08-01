from ...base import SurvoxAPIBase
from ...exception import SurvoxAPINotFound


class SurvoxAPISurveyQuestionnaireModeBase(SurvoxAPIBase):
    mode = 'cati'

    def __init__(self, sid=None, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveyQuestionnaireModeBase, self).__init__(base_url, headers, verbose)
        self.sid = sid

    @property
    def endpoint(self):
        return '/surveys/{sid}/questionnaire/{mode}/'.format(sid=self.sid, mode=self.mode)

    @property
    def upload_endpoint(self):
        return '{base}upload/'.format(base=self.endpoint)

    def get(self):
        try:
            return self.api_get(endpoint=self.endpoint)
        except SurvoxAPINotFound:
            return None

    def upload(self, filename, block_size=100000):
        return self.api_upload(endpoint=self.upload_endpoint, filename=filename, block_size=block_size)

    def delete(self):
        return self.api_delete(endpoint=self.endpoint)


class SurvoxAPISurveyQuestionnaireModeCati(SurvoxAPISurveyQuestionnaireModeBase):
    mode = 'cati'


class SurvoxAPISurveyQuestionnaireModeOnline(SurvoxAPISurveyQuestionnaireModeBase):
    mode = 'online'
