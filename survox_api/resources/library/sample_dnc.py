import os
import json

from ...resources.base import SurvoxAPIBase
from ...resources.exception import SurvoxAPIRuntime, SurvoxAPINotFound
from ...resources.valid import valid_url_field


class SurvoxAPIDncList(SurvoxAPIBase):
    """
    Class to manage DNC lists.
    """

    def __init__(self, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIDncList, self).__init__(base_url, headers, verbose)
        self.url = '/sample/dnc/'

    def list(self):
        """
        Fetch a list of available DNC lists
        :return: list of DNC lists
        """
        return self.api_get(endpoint=self.url)

    def create(self, name, description, dnc_type, account, filename=None, exists_okay=False):
        """
        Create a new DNC list
        :param name: new DNC list name
        :param dnc_type: DNC list type
        :param description: DNC description
        :param account: Survox runtime account to put the DNC list into
        :param filename: csv file containing dnc information
        :param exists_okay: return existing list if True, else raise exception
        :return: dnc list information
        """
        valid, msg = valid_url_field('Do-Not-Contact', name, 1, 256)
        if not valid:
            raise SurvoxAPIRuntime(msg)
        valid_dnc_types = ['phone', 'prefix', 'email']
        if dnc_type not in valid_dnc_types:
            raise SurvoxAPIRuntime('Unknown DNC type "{type}".  Must be one of {opts}'.format(type=dnc_type,
                                                                                              opts=json.loads(
                                                                                                  valid_dnc_types)))
        try:
            s = self.api_get(endpoint='{base}{name}/'.format(base=self.url, name=name))
            if not exists_okay:
                raise SurvoxAPIRuntime('Do-Not-Contact already exists: {name)'.format(name=name))
        except SurvoxAPINotFound:
            s = self.api_post(endpoint=self.url, data={
                'name': name,
                'dnc_type': dnc_type,
                'description': description,
                'account': account
            })
        if s and filename:
            if not os.path.isfile(filename):
                raise SurvoxAPIRuntime('No such filename for Do-Not-Contact: {name)'.format(name=filename))
            x = SurvoxAPIDnc(name, base_url=self.base_url, headers=self.auth_headers, verbose=self.verbose)
            upload = x.upload(filename)
            s['upload_result'] = upload
        return s

    def delete(self):
        """
        delete all DNC lists
        :return: {}
        """
        return self.api_delete(endpoint=self.url)


class SurvoxAPIDnc(SurvoxAPIBase):
    """
    Class for working with a specific DNC list
    """

    def __init__(self, name, base_url=None, headers=None, verbose=True):
        super(SurvoxAPIDnc, self).__init__(base_url, headers, verbose)
        self.name = name
        self.url = '/sample/dnc/{name}/'.format(name=name)
        self.upload_url = "{base}upload/".format(base=self.url)
        self.download_url = "{base}download/".format(base=self.url)

    def get(self):
        try:
            return self.api_get(endpoint=self.url)
        except SurvoxAPINotFound:
            return None

    def set(self, description=None, realtime=None):
        """
        update a DNC entry
        :param description: new description for DNC list
        :param realtime: if True, set DNC list as realtime, unset as realtime if False
        :return: return the DNC list properties
        """
        dnc = self.get()
        if not dnc:
            raise SurvoxAPIRuntime('No DNC available named: {name}'.format(name=self.name))
        if not description and not realtime:
            raise SurvoxAPIRuntime('No properties passed to set for DNC named: {name}'.format(name=self.name))

        changes = {}
        if description and description != dnc['description']:
            changes['description'] = description
        if realtime and realtime != dnc['realtime']:
            changes['realtime'] = realtime

        if changes:
            return self.api_put(endpoint=self.url, data=changes)
        else:
            return dnc

    def delete(self):
        """
        Delete the specified DNC list
        :return:
        """
        return self.api_delete(endpoint=self.url)

    def upload(self, filename, block_size=None):
        """
        Upload records into DNC list
        :param filename: file to upload
        :param block_size: block size of upload
        :return:
        """
        return self.api_upload(self.upload_url, filename, block_size=block_size)

    def download(self, filename):
        """
        Download a dnc file in csv format
        :param filename: file to save as
        :return:
        """
        download_location = self.api_get(self.download_url)
        if not download_location:
            raise SurvoxAPIRuntime('No DNC available for download: {name}'.format(name=self.name))
        return self.api_download(download_location, filename)
