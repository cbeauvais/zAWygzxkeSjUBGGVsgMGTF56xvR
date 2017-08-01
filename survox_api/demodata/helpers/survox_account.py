import re
import os
import subprocess


class SurvoxAccount:
    def __init__(self, account):
        self.account = account
        self.account_settings = self.read_accountfile()
        self.parmfile_settings = self.read_parmfile(self.account_settings['control'])
        self.settings = self.parmfile_settings.copy()
        self.settings.update(self.account_settings)

    @property
    def runtime(self):
        return self.settings['cfmcpath']

    def run(self, command):
        self.set_command_line_env()
        exit_code = subprocess.call(command, shell=True)
        return exit_code

    def read_accountfile(self):
        account_file = '/cfmc/cfg/accounts/{acct}.acct'.format(acct=self.account)
        with open(account_file) as fh:
            content = fh.readlines()
        account_settings = {}
        for line in content:
            line = line.rstrip()
            if line[:1].find('#') < 0 and line != "":
                key, value = line.split(':')
                account_settings[key.strip()] = value.strip()

        required = ['cfmcpath', 'cfmcgo', 'control']
        missing = [x for x in required if x not in account_settings]
        if missing:
            raise RuntimeError(
                'Account file "{acct} missing required parameter(s): {p}'.format(acct=self.account,
                                                                                 p=', '.join(missing)))
        return account_settings

    @staticmethod
    def read_parmfile(controldir):
        parmfile = '{dir}/parmfile'.format(dir=controldir)
        with open(parmfile) as fh:
            content = fh.readlines()
        parmdata = {}
        for line in content:
            line = re.sub("['#]+.*", ' ', line)
            line = line.rstrip()
            if len(line) != 0:
                key, value = re.split('[:=]', line, maxsplit=1, flags=0)
                parmdata[key.strip().lower()] = value.strip()
        return parmdata

    def set_command_line_env(self):
        for k, v in self.settings.items():
            if k != 'comment':
                os.environ[k.replace('~', '')] = v

        cfmc = self.settings['cfmcpath']
        cfmccfg = self.settings['cfmccfg']
        if not cfmc.endswith('/'):
            cfmc += '/'
        if not cfmccfg.endswith('/'):
            cfmccfg += '/'
        os.environ['CFMC'] = cfmc
        os.environ['CFMCCFG'] = cfmccfg
