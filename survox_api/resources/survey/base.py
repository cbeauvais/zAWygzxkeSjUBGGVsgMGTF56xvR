from ..base import SurvoxAPIBase
from ..exception import SurvoxAPIRuntime, SurvoxAPINotFound
from .quota import SurvoxAPISurveyQuotaList, SurvoxAPISurveyQuota
from .sample.sample import SurvoxAPISurveySample
from .questionnaire.base import SurvoxAPISurveyQuestionnaire


class SurvoxAPISurveyList(SurvoxAPIBase):
    """
    Class for survey list operations: api.surveys.xxx()
    """

    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveyList, self).__init__(base_url, headers, verbose)
        self.url = '/surveys/'

    def list(self):
        """
        return a list of surveys from the API
        """
        return self.api_get(endpoint=self.url)

    def status(self):
        """
        return a list of surveys statuses from the API
        """
        return self.api_get(endpoint='/surveys-status/')

    def create(self, survey_info, exists_okay=False):
        """
        Create a new survey
        :param survey_info:  dictionary containing survey information
        :param exists_okay:  if True will silently not create survey if it already exists
        :return: survey information dictionary
        """
        if not survey_info:
            raise SurvoxAPIRuntime('missing required parameter: survey_info')
        try:
            s = self.api_get(endpoint='{base}{sid}/'.format(base=self.url, sid=survey_info['surveycode']))
            if not exists_okay:
                raise SurvoxAPIRuntime('Survey already exists: {sid)'.format(sid=survey_info['surveycode']))
            return s
        except SurvoxAPINotFound:
            pass
        s = self.api_post(endpoint=self.url, data=survey_info)
        return s


class SurvoxAPISurvey(SurvoxAPIBase):
    """
    Class for survey operations
    """

    def __init__(self, sid, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurvey, self).__init__(base_url, headers, verbose)
        self.sid = sid
        self.list_url = '/surveys/'
        self.survey_url = '/surveys/{sid}/'.format(sid=self.sid)

    def get(self):
        """
        Retrieve the details of the given survey
        :return: survey details dictionary or None
        """
        try:
            return self._get_required()
        except SurvoxAPINotFound:
            return None

    def _get_required(self):
        return self.api_get(endpoint=self.survey_url)

    def status(self):
        """
        Fetch status information about survey state
        :return: status dictionary
        """
        l = self.api_get(endpoint='/surveys-status/')
        for x in l:
            if x['surveycode'] == self.sid:
                return x
        return {}

    @property
    def sample(self):
        self._get_required()
        return SurvoxAPISurveySample(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                     verbose=self.verbose)

    @property
    def questionnaire(self):
        self._get_required()
        return SurvoxAPISurveyQuestionnaire(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                            verbose=self.verbose)

    @property
    def quotas(self):
        self._get_required()
        return SurvoxAPISurveyQuotaList(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                        verbose=self.verbose)

    def quota(self, name):
        self._get_required()
        return SurvoxAPISurveyQuota(name, sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                    verbose=self.verbose)
