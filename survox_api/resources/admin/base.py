from ..base import SurvoxAPIBase
from ..exception import SurvoxAPIRuntime
from ..valid import valid_url_field
from .lists import SurvoxAPIAdminLocationList, SurvoxAPIAdminLocation
from .lists import SurvAPIAdminOrgUnitList, SurvAPIAdminOrgUnit
from .lists import SurvAPIAdminLanguageList, SurvAPIAdminLanguage
from .lists import SurvAPIAdminQualificationList, SurvAPIAdminQualification
from .lists import SurvAPIAdminSkillList, SurvAPIAdminSkill
from .lists import SurvAPIAdminSpecialtypeList, SurvAPIAdminSpecialtype

class SurvoxAPIAdmin(SurvoxAPIBase):
    """
    Class to contain API library functionality.  Access it via api.library.dncs.list(), api.library.dncs.create(...),
    api.library.dnc{name}.delete(), etc.
    """

    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIAdmin, self).__init__(base_url, headers, verbose)
        self.url = '/admin/'

    @property
    def locations(self):
        return SurvoxAPIAdminLocationList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def location(self, name):
        valid, msg = valid_url_field('location name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPIAdminLocation(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def organizational_units(self):
        return SurvAPIAdminOrgUnitList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def organizational_unit(self, name):
        valid, msg = valid_url_field('organizational unit name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvAPIAdminOrgUnit(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def languages(self):
        return SurvAPIAdminLanguageList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def language(self, name):
        valid, msg = valid_url_field('language name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvAPIAdminLanguage(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def qualifications(self):
        return SurvAPIAdminQualificationList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def qualification(self, name):
        valid, msg = valid_url_field('qualification name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvAPIAdminQualification(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def skills(self):
        return SurvAPIAdminSkillList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def skill(self, name):
        valid, msg = valid_url_field('skill name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvAPIAdminSkill(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def special_types(self):
        return SurvoxAPIAdminLocationList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def special_type(self, name):
        valid, msg = valid_url_field('special_type name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPIAdminLocation(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

