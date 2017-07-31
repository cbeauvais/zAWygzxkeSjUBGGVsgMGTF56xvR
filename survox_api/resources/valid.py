import re


def valid_url_field(name, value, minlen=1, maxlen=256):
    if len(value) < minlen:
        return False, '{name} too short, must be between {minlen} and {maxlen} characters'.format(name=name,
                                                                                                  minlen=minlen,
                                                                                                  maxlen=maxlen)
    if len(value) > maxlen:
        return False, '{name} too long, must be between {minlen} and {maxlen} characters'.format(name=name,
                                                                                                 minlen=minlen,
                                                                                                 maxlen=maxlen)
    if not value[0].isalpha():
        return False, '{name} must start with a letter'.format(name=name)
    search = re.compile(r'[^a-z0-9_]').search
    if bool(search(value.lower())):
        return False, '{name} must contain only characters in "{allowed}"'.format(name=name, allowed='[a-z0-9_]')
    return True, value.lower()
