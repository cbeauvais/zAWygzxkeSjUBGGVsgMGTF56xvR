from ..base import SurvoxAPIBase
from ..exception import SurvoxAPIRuntime
from ..valid import valid_url_field
from .sample_dnc import SurvoxAPIDncList, SurvoxAPIDnc
from .sample_map import SurvoxAPISampleMapList, SurvoxAPISampleMap
from .sample_setup_rules import SurvoxAPISampleSetupRulesList, SurvoxAPISampleSetupRules
from .sample_calling_rules import SurvoxAPISampleCallingRulesList, SurvoxAPISampleCallingRules


class SurvoxAPILibrary(SurvoxAPIBase):
    """
    Class to contain API library functionality.  Access it via api.library.dncs.list(), api.library.dncs.create(...),
    api.library.dnc{name}.delete(), etc.
    """

    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPILibrary, self).__init__(base_url, headers, verbose)
        self.url = '/surveys/'

    @property
    def dncs(self):
        return SurvoxAPIDncList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def dnc(self, name):
        valid, msg = valid_url_field('DNC setup name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPIDnc(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def sample_maps(self):
        return SurvoxAPISampleMapList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def sample_map(self, name):
        valid, msg = valid_url_field('Sample map name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPISampleMap(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def sample_setup_rules(self):
        return SurvoxAPISampleSetupRulesList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def sample_setup_rule(self, name):
        valid, msg = valid_url_field('Sample setup name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPISampleSetupRules(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    @property
    def sample_calling_rules(self):
        return SurvoxAPISampleCallingRulesList(base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)

    def sample_calling_rule(self, name):
        valid, msg = valid_url_field('Sample setup name', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        return SurvoxAPISampleCallingRules(name, base_url=self.base_url, headers=self.auth_headers,
                                           verbose=self.verbose)
