from .modes import SurvoxAPISurveyQuestionnaireModeCati, SurvoxAPISurveyQuestionnaireModeOnline, \
    SurvoxAPISurveyQuestionnaireModeBase


class SurvoxAPISurveyQuestionnaire(SurvoxAPISurveyQuestionnaireModeBase):
    def __init__(self, sid=None, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveyQuestionnaire, self).__init__(sid, base_url, headers, verbose)
        self.sid = sid

    @property
    def cati(self):
        return SurvoxAPISurveyQuestionnaireModeCati(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                                    verbose=self.verbose)

    @property
    def online(self):
        return SurvoxAPISurveyQuestionnaireModeOnline(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                                      verbose=self.verbose)
