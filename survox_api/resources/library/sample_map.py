from survox_api.resources.base import SurvoxAPIBase
from survox_api.resources.exception import SurvoxAPIRuntime, SurvoxAPINotFound
from survox_api.resources.valid import valid_url_field


class SurvoxAPISampleMapList(SurvoxAPIBase):
    """
    Class that works with sample setup rules templates
    """
    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISampleMapList, self).__init__(base_url, headers, verbose)
        self.url = '/sample/map/'

    def list(self):
        """
        Fetch a list of sample setup rule templates
        :return:
        """
        return self.api_get(endpoint=self.url)

    def create(self, mapping, exists_okay=False):
        """
        Create a new sample setup rule template
        :param mapping: dictionary containing the mapping from the csvfile to the survox variables
        :param exists_okay: if rule exists and True skip create, otherwise raise exception
        :return: calling rule
        """
        valid, msg = valid_url_field('Sample map name', mapping['name'], 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        try:
            s = self.api_get(endpoint='{base}{name}/'.format(base=self.url, name=mapping['name']))
            if not exists_okay:
                raise SurvoxAPIRuntime('Sample map template already exists: {name)'.format(name=mapping['name']))
            return s
        except SurvoxAPINotFound:
            s = self.api_post(endpoint=self.url, data=mapping)
        return s

    def delete(self):
        """
        Delete all sample setup rules
        :return: {}
        """
        return self.api_delete(endpoint=self.url)


class SurvoxAPISampleMap(SurvoxAPIBase):
    """
    Class to work with specific sample setup rule template
    """
    def __init__(self, name, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISampleMap, self).__init__(base_url, headers, verbose)
        self.name = name
        self.url = '/sample/map/{name}/'.format(name=name)

    def get(self):
        """
        Fetch sample setup rule template
        :return: sample setup rule template, or None
        """
        try:
            return self.api_get(endpoint=self.url)
        except SurvoxAPINotFound:
            return None

    def set(self, sample_map):
        """
        Update the sample setup rule template
        :param sample_map: new sample map dictionary
        :return: updated sample setup rule
        """
        existing = self.get()
        if not existing:
            raise SurvoxAPIRuntime('No sample map template: {name}'.format(name=self.name))
        return self.api_put(endpoint=self.url, data=sample_map)

    def delete(self):
        """
        Delete the sample setup rule
        :return: {}
        """
        return self.api_delete(endpoint=self.url)
