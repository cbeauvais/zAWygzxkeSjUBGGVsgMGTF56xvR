from survox_api.resources.base import SurvoxAPIBase
from survox_api.resources.exception import SurvoxAPIRuntime, SurvoxAPINotFound
from survox_api.resources.valid import valid_url_field


class SurvoxAPISampleCallingRulesList(SurvoxAPIBase):
    """
    Class that works with sample calling rules templates
    """
    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISampleCallingRulesList, self).__init__(base_url, headers, verbose)
        self.url = '/sample/calling-rules/'

    def list(self):
        """
        Fetch a list of calling rules templates
        :return: list of calling rules templates
        """
        return self.api_get(endpoint=self.url)

    def create(self, rule, exists_okay=False):
        """
        Create a new calling rule template
        :param rule: parameters for the rule
        :param exists_okay: if rule exists and True skip create, otherwise raise exception
        :return: calling rule
        """
        valid, msg = valid_url_field('Sample calling rule', rule['name'], 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        try:
            s = self.api_get(endpoint='{base}{name}/'.format(base=self.url, name=rule['name']))
            if not exists_okay:
                raise SurvoxAPIRuntime('Sample calling rule already exists: {name)'.format(name=rule['name']))
            return s
        except SurvoxAPINotFound:
            pass
        s = self.api_post(endpoint=self.url, data=rule)
        return s

    def delete(self):
        """
        Delete all calling rule templates
        :return: {}
        """
        return self.api_delete(endpoint=self.url)


class SurvoxAPISampleCallingRules(SurvoxAPIBase):
    """
    Class to work with specific sample calling rule template
    """
    def __init__(self, name, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISampleCallingRules, self).__init__(base_url, headers, verbose)
        self.name = name
        self.url = '/sample/calling-rules/{name}/'.format(name=name)

    def get(self):
        """
        Fetch sample calling rule template
        :return: calling rule template, or None
        """
        try:
            return self.api_get(endpoint=self.url)
        except SurvoxAPINotFound:
            return None

    def set(self, rule):
        """
        Update the sample calling rule template
        :param rule: new sample calling rule parameters
        :return: updated sample calling rule
        """
        current_rule = self.get()
        if not current_rule:
            raise SurvoxAPIRuntime('No sample calling rule: {name}'.format(name=self.name))
        return self.api_put(endpoint=self.url, data=rule)

    def delete(self):
        """
        Delete the sample calling rule
        :return: {}
        """
        return self.api_delete(endpoint=self.url)
