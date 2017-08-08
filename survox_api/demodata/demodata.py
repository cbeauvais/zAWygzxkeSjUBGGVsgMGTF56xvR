#!/usr/bin/python3

import json
import os
import errno
import stat
import shutil
import subprocess
from pprint import pprint

from survox_api.demodata.helpers.survox_account import SurvoxAccount
from survox_api.demodata.helpers.quota_converter import QuotaConverter
from survox_api.survox_api import SurvoxAPI

base_directory = os.path.dirname(__file__)


def ops_manager_install(account, api_key):
    return installer(account=account, api_key=api_key, install_these={
        'clients': ['survoxhealth'],
        'dncs': ['global'],
        'sample_setup_rules': ['my_default_us'],
        'sample_calling_rules': ['my_basic'],
        'surveys': ['ph_waittime', 'rr_customer_care'],
        'delete_sample': True
    })


def installer(account, api_key, install_these):
    api = SurvoxAPI('localhost', api_key)
    cli = SurvoxAccount(account)

    if 'clients' in install_these and install_these['clients']:
        api_install_clients(api, install_these['clients'])
    if 'dncs' in install_these and install_these['dncs']:
        api_install_dncfiles(api, install_these['dncs'])
    if 'sample_setup_rules' in install_these and install_these['sample_setup_rules']:
        api_install_setup_rule_templates(api, install_these['sample_setup_rules'])
    if 'sample_calling_rules' in install_these and install_these['sample_calling_rules']:
        api_install_calling_rule_templates(api, install_these['sample_calling_rules'])
    if 'surveys' in install_these and install_these['surveys']:
        for surveycode in install_these['surveys']:
            survey_conf = read_config('survey', surveycode)
            api_install_surveys(api, survey_conf, install_these.get('delete_sample', True))
            command_line_install_survey(cli, survey_conf)
    print("All Done!")


def read_config(location, file):
    filename = os.path.join(base_directory, 'config', location, file)
    if not filename.endswith('.json'):
        filename += '.json'
    print("Reading config: {file}".format(file=filename))
    return json.loads(open(filename).read())


def read_survey_config(client, surveycode, file):
    filename = survey_datafile(client, surveycode, file)
    print("Reading config: {file}".format(file=filename))
    return json.loads(open(filename).read())


def datafile(file):
    return os.path.join(base_directory, 'data', file)


def survey_datafile(client, surveycode, file):
    if file:
        return os.path.join(base_directory, 'data', 'surveys', client, surveycode, file)
    else:
        return os.path.join(base_directory, 'data', 'surveys', client, surveycode)


def api_install_clients(api, client_list):
    for client in client_list:
        print("Creating client: {c}".format(c=client))
        conf = read_config('client', client)
        c = api.clients.create(conf['client'], conf['name'], exists_okay=True)
        print(c)


def api_install_setup_rule_templates(api, setup_rules_list):
    for rule in setup_rules_list:
        print("Creating setup rule template: {c}".format(c=rule))
        conf = read_config('sample_setup_rules', rule)
        x = api.library.sample_setup_rules.create(conf, exists_okay=True)
        pprint(x)


def api_install_calling_rule_templates(api, calling_rules_list):
    for rule in calling_rules_list:
        print("Creating setup rule template: {c}".format(c=rule))
        conf = read_config('sample_calling_rules', rule)
        x = api.library.sample_calling_rules.create(conf, exists_okay=True)
        pprint(x)


def api_install_dncfiles(api, dnc_list):
    for dnc in dnc_list:
        conf = read_config('dnc', dnc)
        data = conf['create_data']
        dnc_sample = datafile(conf['dnc_file'])
        print("Installing dnc file: {dnc} - {file}".format(dnc=dnc, file=dnc_sample))
        x = api.library.dncs.create(data['name'], data['description'], data['dcn_type'], data['account'],
                                    filename=dnc_sample, exists_okay=True)
        pprint(x)


def api_install_surveys(api, survey_info, delete=True):
    surveycode = survey_info['create_data']['surveycode']

    print("Installing survey: {s}".format(s=surveycode))
    c = api.surveys.create(survey_info['create_data'], exists_okay=True)
    print(c)

    # install the sample, if not already there
    if delete:
        api.survey(surveycode).sample.delete()
    c = api.survey(surveycode).status()
    if not c['status']['sample']:
        api_install_survey_sample(api, survey_info['create_data']['client'], surveycode, survey_info['survey_sample'])
    else:
        print("sample already exists for {s}".format(s=surveycode))
        print(c)

    # install quotas, set survox_completes
    api_install_survey_quotas(api, survey_info['create_data']['client'], surveycode, survey_info['quota_file'])
    qlist = api.survey(surveycode).quotas.list()
    if 'survox_complete' not in qlist:
        api.survey(surveycode).quotas.create([{
            'name': 'survox_complete',
            'current': 0,
            'target': survey_info['create_data']['survox_complete_target'],
            'total': survey_info['survox_complete_total']
        }])
    api.survey(surveycode).quota('survox_complete').set(total=survey_info['survox_complete_total'])
    print(" --- survey {s} installed".format(s=surveycode))


def api_install_survey_sample(api, client, surveycode, sample_configfile):
    conf = read_survey_config(client, surveycode, sample_configfile)
    csv_sample = survey_datafile(client, surveycode, os.path.join('sample', conf['sample_file']))
    print("Uploading csv sample file: {file}".format(file=csv_sample))

    api.survey(surveycode).sample.add(csv_sample, sample_map=conf['sample_map'], setup_rules=conf['sample_setup_rules'],
                                      calling_rules=conf['sample_calling_rules'], exists_okay=True)
    c = api.survey(surveycode).status()
    print(c)


def api_install_survey_quotas(api, client, surveycode, quota_aqu):
    quota_file = survey_datafile(client, surveycode, quota_aqu)
    print("Installing/updating quotas from file: {file}".format(file=quota_file))
    qlist = QuotaConverter.from_aqu(quota_file)
    print("    {n} quotas".format(n=len(qlist)))
    created = api.survey(surveycode).quotas.create(qlist)
    print("    {n} quotas created - updating {u} ...".format(n=len(created), u=len(qlist) - len(created)))
    created_qnames = [x['name'] for x in created]
    for q in qlist:
        if not q['name'] in created_qnames:
            api.survey(surveycode).quota(q['name']).set(quota=q)


def command_line_install_survey(cli, survey_info):
    print("  updating {s} from command line".format(s=survey_info['create_data']['surveycode']))

    sourcebase = os.path.join(os.path.dirname(__file__), 'data', 'surveys')
    targetbase = os.path.join(cli.runtime, 'surveys')

    sourcedir = os.path.join(sourcebase, survey_info['create_data']['client'], survey_info['create_data']['surveycode'])
    targetdir = os.path.join(targetbase, survey_info['create_data']['client'], survey_info['create_data']['surveycode'])

    print("       copying files from {s} to {t}".format(s=sourcedir, t=targetdir))
    for here, dirs, files in os.walk(sourcedir):
        there = here.replace(sourcedir, targetdir)
        try:
            os.makedirs(there)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        for f in files:
            src = os.path.join(here, f)
            tgt = os.path.join(there, f)
            shutil.copyfile(src, tgt)
            shutil.copystat(src, tgt)
    if os.path.isfile(os.path.join(targetdir, 'configure_survey.sh')):
        run_command_line_script(cli, targetdir, 'configure_survey.sh')


def run_command_line_script(cli, survey_dir, script):
    cli.set_command_line_env()
    print("   Running " + script)
    script_path = os.path.join(survey_dir, script)
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)
    subprocess.call(script_path, shell=True, cwd=survey_dir)


if __name__ == '__main__':
    ops_manager_install('survox', 'an_api_key')
