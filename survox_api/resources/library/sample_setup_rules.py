from survox_api.resources.base import SurvoxAPIBase
from survox_api.resources.exception import SurvoxAPIRuntime, SurvoxAPINotFound
from survox_api.resources.valid import valid_url_field


class SurvoxAPISampleSetupRulesList(SurvoxAPIBase):
    """
    Class that works with sample setup rules templates
    """
    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISampleSetupRulesList, self).__init__(base_url, headers, verbose)
        self.url = '/sample/setup-rules/'

    def list(self):
        """
        Fetch a list of sample setup rule templates
        :return:
        """
        return self.api_get(endpoint=self.url)

    def create(self, rule, exists_okay=False):
        """
        Create a new sample setup rule template
        :param rule: parameters for the rule
        :param exists_okay: if rule exists and True skip create, otherwise raise exception
        :return: calling rule
        """
        valid, msg = valid_url_field('Sample setup rule', rule['name'], 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        try:
            s = self.api_get(endpoint='{base}{name}/'.format(base=self.url, name=rule['name']))
            if not exists_okay:
                raise SurvoxAPIRuntime('Sample setup rule already exists: {name)'.format(name=rule['name']))
            return s
        except SurvoxAPINotFound:
            s = self.api_post(endpoint=self.url, data=rule)
        return s

    def delete(self):
        """
        Delete all sample setup rules
        :return: {}
        """
        return self.api_delete(endpoint=self.url)


class SurvoxAPISampleSetupRules(SurvoxAPIBase):
    """
    Class to work with specific sample setup rule template
    """
    def __init__(self, name, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISampleSetupRules, self).__init__(base_url, headers, verbose)
        self.name = name
        self.url = '/sample/setup-rules/{name}/'.format(name=name)

    def get(self):
        """
        Fetch sample setup rule template
        :return: sample setup rule template, or None
        """
        try:
            return self.api_get(endpoint=self.url)
        except SurvoxAPINotFound:
            return None

    def set(self, rule):
        """
        Update the sample setup rule template
        :param rule: new sample setup rule parameters
        :return: updated sample setup rule
        """
        current_rule = self.get()
        if not current_rule:
            raise SurvoxAPIRuntime('No sample setup rule: {name}'.format(name=self.name))
        return self.api_put(endpoint=self.url, data=rule)

    def delete(self):
        """
        Delete the sample setup rule
        :return: {}
        """
        return self.api_delete(endpoint=self.url)
