from ...base import SurvoxAPIBase


class SurvoxAPISurveySampleSelection(SurvoxAPIBase):
    def __init__(self, sid=None, base_url=None, headers=None, verbose=True):
        super(SurvoxAPISurveySampleSelection, self).__init__(base_url, headers, verbose)
        self.sid = sid
        self.endpoint = '/surveys/{sid}/sample-selection/'.format(sid=self.sid)

    def _selection_url(self, action):
        return '{base}{action}/'.format(base=self.endpoint, action=action)

    def list(self, selection):
        return self.api_post(endpoint=self._selection_url('list'), json=selection)

    def download(self, selection, filename):
        preview = self.list(selection)
        download_link = '{base}list/download/?fid={fid}'.format(base=self.endpoint, fid=preview['fid'])
        return self.api_download(endpoint=download_link, filename=filename)

    def hide(self, selection, name=None):
        select = {"hide": 'hide'}
        select.update(selection)
        if name:
            select['name'] = name
        return self.api_post(endpoint=self._selection_url('hide'), json=select)

    def unhide(self, selection, name=None):
        select = {"hide": 'unhide'}
        select.update(selection)
        if name:
            select['name'] = name
        return self.api_post(endpoint=self._selection_url('hide'), json=select)

    def resolve(self, selection, resolution_code):
        select = {"resolution_code": resolution_code}
        select.update(selection)
        return self.api_post(endpoint=self._selection_url('resolve'), json=select)

    def gather_special(self, selection, sort_by_timeezone=False):
        select = {"sort_by_timezone": sort_by_timeezone}
        select.update(selection)
        return self.api_post(endpoint=self._selection_url('gather-special'), json=select)

    def delete(self, selection):
        select = {'delete': True}
        select.update(selection)
        return self.api_post(endpoint=self._selection_url('delete'), json=select)

    def remove_attempts(self, selection, attempts=None):
        if not attempts:
            attempts = 'last'
        select = {"attempts": attempts}
        select.update(selection)
        return self.api_post(endpoint=self._selection_url('remove-attempts'), json=select)

    def replicate(self, selection, replicate):
        select = {'replicate': replicate}
        select.update(selection)
        return self.api_post(endpoint=self._selection_url('replicate'), json=select)

    def return_owned(self, selection):
        select = {'return_owned': True}
        select.update(selection)
        return self.api_post(endpoint=self._selection_url('return-owned'), json=select)
