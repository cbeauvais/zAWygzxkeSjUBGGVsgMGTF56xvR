class SurvoxAPIException(RuntimeError):
    """
    superclass for custom survox exceptions so we can catch them all
    """

    def __init__(self, method, url, response, **kwargs):
        self.method = method
        self.url = url
        self.response = response
        self.kwargs = kwargs

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def text(self):
        return self.response.text

    def __str__(self):
        return 'Error[{code}] - {method} {url} - {text}'.format(code=self.response.status_code, method=self.method,
                                                                url=self.url, text=self.response.text)


class SurvoxAPIRuntime(RuntimeError):
    """
    superclass for custom survox exceptions so we can catch them all
    """

    def __init__(self, text, **kwargs):
        self.text = text
        self.kwargs = kwargs

    def __str__(self):
        return 'Error[0] - {text}'.format(text=self.text)


class SurvoxAPIMissingParameter(SurvoxAPIRuntime):
    def __init__(self, parameter):
        text = "missing required parameter - {p}".format(p=parameter)
        super(SurvoxAPIMissingParameter, self).__init__(text)


class SurvoxAPINotFound(SurvoxAPIException):
    pass
