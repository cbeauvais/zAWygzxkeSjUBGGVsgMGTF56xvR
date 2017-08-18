from survox_api.resources.base import SurvoxAPIBase
from survox_api.resources.exception import SurvoxAPIRuntime, \
    SurvoxAPIMissingParameter, SurvoxAPINotFound
from survox_api.resources.valid import valid_url_field
from survox_api.resources.client.credentials import SurvoxAPIClientCredentialList, \
    SurvoxAPIClientCredential


class SurvoxAPIAdminLocationList(SurvoxAPIBase):
    capability = 'location'
    list_endpoint = '/admin/locations/'

    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIAdminLocationList, self).__init__(base_url, headers, verbose)

    def list(self):
        return self.api_get(endpoint=self.list_endpoint)

    def create(self, name, description, exists_okay=False):
        valid, msg = valid_url_field('{cap} name'.format(cap=self.capability), name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        try:
            s = self.api_get(endpoint='{base}{name}/'.format(base=self.list_endpoint, name=name))
            if not exists_okay:
                raise SurvoxAPIRuntime('{cap} already exists: {name)'.format(cap=self.capability, name=name))
            return s
        except SurvoxAPINotFound:
            pass
        s = self.api_post(endpoint=self.list_endpoint, data={
            'name': name,
            'description': description
        })
        return s


class SurvoxAPIAdminLocation(SurvoxAPIBase):
    capability = 'location'
    list_endpoint = '/admin/locations/'

    def __init__(self, name, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIAdminLocation, self).__init__(base_url, headers, verbose)
        self.name = name

    @property
    def endpoint(self):
        return '{base}{name}'.format(base=self.list_endpoint, name=self.name)

    def get(self):
        try:
            return self.api_get(endpoint=self.endpoint)
        except SurvoxAPINotFound:
            return None

    def set(self, data):
        """
        update a client entry
        :param data: dictionary for list {name: item-name, description: item-description}
        :return: return the item added
        """
        if not data:
            raise SurvoxAPIMissingParameter(self.capability)
        c = self.get()
        if not c:
            raise SurvoxAPIRuntime('No {cap} available named: {name}'.format(cap=self.capability, name=self.name))
        return self.api_put(endpoint=self.endpoint, data=data)

    def delete(self):
        return self.api_delete(endpoint=self.endpoint)


class SurvAPIAdminOrgUnitList(SurvoxAPIAdminLocationList):
    capability = 'location'
    list_endpoint = '/admin/organizational-unit/'


class SurvAPIAdminOrgUnit(SurvoxAPIAdminLocation):
    capability = 'location'
    list_endpoint = '/admin/organizational-unit/'


class SurvAPIAdminLanguageList(SurvoxAPIAdminLocationList):
    capability = 'language'
    list_endpoint = '/admin/languages/'


class SurvAPIAdminLanguage(SurvoxAPIAdminLocation):
    capability = 'language'
    list_endpoint = '/admin/languages/'


class SurvAPIAdminQualificationList(SurvoxAPIAdminLocationList):
    capability = 'location'
    list_endpoint = '/admin/qualifications/'


class SurvAPIAdminQualification(SurvoxAPIAdminLocation):
    capability = 'location'
    list_endpoint = '/admin/qualifications/'


class SurvAPIAdminSkillList(SurvoxAPIAdminLocationList):
    capability = 'skills'
    list_endpoint = '/admin/skills/'


class SurvAPIAdminSkill(SurvoxAPIAdminLocation):
    capability = 'skills'
    list_endpoint = '/admin/skills/'


class SurvAPIAdminSpecialtypeList(SurvoxAPIAdminLocationList):
    capability = 'skills'
    list_endpoint = '/admin/skills/'


class SurvAPIAdminSpecialtype(SurvoxAPIAdminLocation):
    capability = 'skills'
    list_endpoint = '/admin/skills/'

