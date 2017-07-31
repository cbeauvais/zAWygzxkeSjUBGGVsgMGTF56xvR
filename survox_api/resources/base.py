import hashlib
import os
import errno
import tempfile
from json import dumps as json_dumps
import requests

from .exception import SurvoxAPIException, SurvoxAPINotFound


class SurvoxAPIBase:
    """
    Base class to use requests to interact with the Survox API
    """

    def __init__(self, base_url, headers, verbose=True):
        self.base_url = base_url
        self.auth_headers = headers
        self.verbose = verbose

    def api_get(self, endpoint, headers=None, full_response=False):
        """
        Make a GET request to the specified endpoint
        :param endpoint: api endpoint
        :param headers: extra headers to pass with request
        :param full_response: return the requests response structure
        :return: api response data, or full requests response structure
        """
        endpoint, headers = self._update_request_info('GET', endpoint, headers)
        r = requests.get(url=endpoint, headers=headers)
        if full_response:
            return r
        return self._check_response(r, 'GET', endpoint)

    def api_post(self, endpoint, data=None, json=None, headers=None, full_response=False):
        """
        Make a POST request to the specified endpoint
        :param endpoint: api endpoint
        :param data: data to post
        :param json: data to post in json format
        :param headers: extra headers to pass with request
        :param full_response: return the requests response structure
        :return: api response data, or full requests response structure
        """
        endpoint, headers = self._update_request_info('POST', endpoint, headers)
        if json:
            headers.update({"Content-Type": "application/json"})
            r = requests.post(endpoint, data=json_dumps(json), headers=headers)
        else:
            r = requests.post(url=endpoint, data=data, headers=headers)
        if full_response:
            return r
        return self._check_response(r, 'POST', endpoint)

    def api_put(self, endpoint, data=None, json=None, headers=None, files=None, full_response=False):
        """
        Make a PUT request to the specified endpoint
        :param endpoint: api endpoint
        :param data: data to post, works for simple dictionaries
        :param json: data to post using json for nested dictionaries, etc.
        :param headers: extra headers to pass with request
        :param files: files object to upload
        :param full_response: return the requests response structure
        :return: api response data, or full requests response structure
        """
        endpoint, headers = self._update_request_info('PUT', endpoint, headers)
        if files:
            return requests.put(url=endpoint, data=data, headers=headers, files=files)
        if json:
            r = requests.put(url=endpoint, json=json_dumps(json), headers=headers)
        else:
            r = requests.put(url=endpoint, data=data, headers=headers)
        if full_response:
            return r
        return self._check_response(r, 'PUT', endpoint)

    def api_delete(self, endpoint, headers=None, full_response=False):
        """
        Make a DELETE request to the specified endpoint
        :param endpoint: api endpoint
        :param headers: extra headers to pass with request
        :param full_response: return the requests response structure
        :return: api response data, or full requests response structure
        """
        endpoint, headers = self._update_request_info('DELETE', endpoint, headers)
        r = requests.delete(url=endpoint, headers=headers)
        if full_response:
            return r
        return self._check_response(r, 'DELETE', endpoint)

    def _update_request_info(self, method, endpoint, headers):
        if not (endpoint.startswith(self.base_url) or endpoint.startswith("http")):
            if not endpoint.startswith('/'):
                endpoint = self.base_url + '/' + endpoint
            else:
                endpoint = self.base_url + endpoint
        if headers:
            headers.update(self.auth_headers)
        else:
            headers = self.auth_headers
        if self.verbose:
            print('Request {method} {endpoint}'.format(method=method, endpoint=endpoint))
        return endpoint, headers

    def _check_response(self, r, method, endpoint):
        if self.verbose:
            print('Response {method} {endpoint} {result} {length}'.format(method=method, endpoint=endpoint,
                                                                          result=r.status_code, length=len(r.text)))
        if not 200 <= r.status_code < 300:
            if r.status_code == 404:
                raise SurvoxAPINotFound(method, endpoint, r)
            else:
                raise SurvoxAPIException(method, endpoint, r)
        try:
            payload = r.json()
        except Exception as e:
            raise SurvoxAPIException(method, endpoint, r)
        if 'status' not in payload or payload['status'] != 'success':
            raise SurvoxAPIException(method, endpoint, r)
        if 'data' not in payload:
            raise SurvoxAPIException(method, endpoint, r)
        return payload['data']

    def api_upload(self, endpoint, filename, block_size=None):
        """
        Make a DELETE request to the specified endpoint
        :param endpoint: api endpoint
        :param filename: name of the file to upload
        :param block_size: max size of a file block to send at a time
        :return: api response data, or full requests response structure
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

        hash_md5 = hashlib.md5()
        file_size = os.path.getsize(filename)
        upload_name = os.path.basename(filename)
        if not block_size:
            block_size = 1000000

        with open(filename, "rb") as f:
            offset = 0
            for block in iter(lambda: f.read(block_size), b""):
                hash_md5.update(block)
                temp = tempfile.NamedTemporaryFile()
                temp.write(block)
                temp.seek(0)
                chunk_end = offset + len(block)
                my_headers = {
                    'CONTENT-RANGE': "bytes {offset}-{chunk_end}/{filesize}".format(offset=offset,
                                                                                    chunk_end=chunk_end,
                                                                                    filesize=file_size)
                }
                cur_data = {'filename': upload_name}
                file = [('file', (temp.name, block))]
                res = self.api_put(endpoint=endpoint, headers=my_headers, data=cur_data, files=file, full_response=True)
                temp.close()
                try:
                    content = res.json()
                except ValueError:
                    raise RuntimeError('Content' + res.text)
                if content['status'] != "success":
                    raise RuntimeError(content['data'])
                offset = chunk_end
                endpoint = content['data']['url']

        md5hash = hash_md5.hexdigest()

        # Finalize this thing
        cur_data = {"md5": "{hash}".format(hash=md5hash)}
        res = self.api_post(endpoint=endpoint, data=cur_data, full_response=True)
        try:
            content = res.json()
        except ValueError:
            raise RuntimeError('Content' + res.text)

        if content['status'] != "success":
            raise RuntimeError(content['data'])
        return content['data']

    def api_download(self, endpoint, filename, headers=None):
        """
        Download a file from the API endpoint
        :param endpoint: api endpoint
        :param filename:  file to save response in
        :param headers: any additional headers to send when making request
        :return: None
        """
        endpoint, headers = self._update_request_info('DOWNLOAD', endpoint, headers)
        return_headers = {}
        with open(filename, 'wb') as handle:
            response = requests.get(endpoint, headers=headers, stream=True)
            if not response.ok:
                raise RuntimeError("Unable to download file from {url}".format(url=endpoint))
            for h, v in response.headers.items():
                return_headers[h] = v
            for block in response.iter_content(1024):
                handle.write(block)
        return return_headers
