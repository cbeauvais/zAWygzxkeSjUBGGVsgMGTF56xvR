import ntpath

from ...base import SurvoxAPIBase
from .map import SurvoxAPISurveySampleMap
from .setup_rules import SurvoxAPISurveySampleSetupRules
from .calling_rules import SurvoxAPISurveySampleCallingRules
from .selection import SurvoxAPISurveySampleSelection


class SurvoxAPISurveySample(SurvoxAPIBase):
    def __init__(self, sid=None, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveySample, self).__init__(base_url, headers, verbose)
        self.sid = sid
        self.endpoint = '/surveys/{sid}/sample/'.format(sid=self.sid)
        self.upload_endpoint = '{base}upload/'.format(base=self.endpoint)
        self.import_endpoint = '{base}import/'.format(base=self.endpoint)
        self.fields_endpoint = '{base}fields/'.format(base=self.endpoint)
        self.rebuild_endpoint = '{base}rebuild/'.format(base=self.endpoint)
        self.repair_endpoint = '{base}repair/'.format(base=self.endpoint)
        self.recover_endpoint = '{base}recover/'.format(base=self.endpoint)

    def get(self):
        return self.api_get(endpoint=self.endpoint)

    def delete(self):
        return self.api_delete(endpoint=self.endpoint)

    def upload(self, filename, block_size=100000):
        return self.api_upload(endpoint=self.upload_endpoint, filename=filename, block_size=block_size)

    def import_csv(self, filename):
        return self.api_post(endpoint=self.import_endpoint, data={'samplefile': ntpath.basename(filename)})

    def fields(self, system=False):
        endpoint = '{base}?system={system}'.format(base=self.fields_endpoint, system=system)
        return self.api_get(endpoint=endpoint)

    def rebuild(self):
        return self.api_post(endpoint=self.rebuild_endpoint, data={})

    def repair(self):
        return self.api_post(endpoint=self.repair_endpoint, data={})

    def recover(self):
        return self.api_post(endpoint=self.recover_endpoint, data={})

    @property
    def map(self):
        return SurvoxAPISurveySampleMap(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                        verbose=self.verbose)

    @property
    def setup_rules(self):
        return SurvoxAPISurveySampleSetupRules(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                               verbose=self.verbose)

    @property
    def calling_rules(self):
        return SurvoxAPISurveySampleCallingRules(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                                 verbose=self.verbose)

    @property
    def selection(self):
        return SurvoxAPISurveySampleSelection(sid=self.sid, base_url=self.base_url, headers=self.auth_headers,
                                              verbose=self.verbose)

    def add(self, filename, sample_map, setup_rules, calling_rules, exists_okay=False, block_size=100000):
        if self.verbose:
            print('uploading sample file: {file}'.format(file=filename))
        upload_results = self.upload(filename=filename, block_size=block_size)
        if self.verbose:
            print('uploading sample map: {x}'.format(x=sample_map))
        map_results = self.map.create(sample_map, exists_okay=exists_okay)
        if self.verbose:
            print('uploading sample setup: {x}'.format(x=setup_rules))
        setup_results = self.setup_rules.create(setup_rules, exists_okay=exists_okay)
        if self.verbose:
            print('uploading sample calling rules: {x}'.format(x=calling_rules))
        calling_results = self.calling_rules.create(calling_rules, exists_okay=exists_okay)
        if self.verbose:
            print('generating sample from file: {x}'.format(x=filename))
        import_results = self.import_csv(filename)
        return {
            'sample_upload_result': upload_results,
            'sample_map_result': map_results,
            'sample_setup_rules_result': setup_results,
            'sample_calling_rules_result': calling_results,
            'sample_import_result': import_results,
        }
