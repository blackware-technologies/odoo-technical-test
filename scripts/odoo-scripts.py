#!/usr/bin/env python3
import sys
import xmlrpc.client
import argparse
import pprint
from ast import literal_eval


pp = pprint.pprint
# run script with --help or -h for help
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', help='Print logs by default',
                    default=True, action='store_false')
parser.add_argument('--database', '-d',
                    help='Odoo database name', type=str, default='odoo')
parser.add_argument('--username', '-u', help='Admin username',
                    type=str, default='admin')
parser.add_argument('--password', '-p', help='Admin password',
                    type=str, default='admin')
parser.add_argument('--host', help='Host url', type=str,
                    default='http://odoo:8069')
parser.add_argument('--timezone', '-t',
                    help='Default timezone ex: "America/Montreal"', type=str, default='')
parser.add_argument('--language', '-l',
                    help='Additional language code ex: "fr_CA"', type=str, default='')
parser.add_argument('--set-default-language', '-dl', help='Set default language in all users', default=False,
                    action='store_true')
parser.add_argument('--access', '-a', help='Set default access rights to true',
                    default=False, action='store_true')
parser.add_argument(
    '--model', '-m', help='Model you wish to fetch. Requires ids', type=str, default='')
parser.add_argument(
    '--ids', '-i', help='Ids separated by a comma. Requires a model. Ex.:  -i 1,2,3', type=str, default='')
parser.add_argument(
    '--filter', '-f', help='filter to search with', type=str, default='')
parser.add_argument(
    '--kwargs', '-k', help="Dictionary with kwargs. Ex.  -k \"{'fields':['name']}\"", type=str, default='{}')


try:
    args = parser.parse_args()
except:
    raise SystemExit
verbose = args.verbose
db = args.database
username = args.username
password = args.password
host = args.host
tz = args.timezone
lang = args.language
sdl = args.set_default_language
dar = args.access
model = args.model
ids = args.ids
filter = args.filter
kwargs = args.kwargs


if (model and (not ids and not filter)) or (ids and not model):
    pp(
        'To fetch a record, both a model and at least one id is required')
    raise SystemExit
if kwargs:
    kwargs = literal_eval(kwargs)
if filter:
    filter = literal_eval(filter)


def _print(*args, **kwargs):
    if verbose:
        pp(*args, **kwargs)


"""
Start Execution 
"""

# Get client and authenticate
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(host))
try:
    uid = common.authenticate(db, username, password, {})
except Exception as e:
    pp(e)
    raise SystemExit
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(host))


def execute(model_name, method_name, params=[], key_params={}):
    try:
        output = models.execute_kw(
            db, uid, password, model_name, method_name, params, key_params)
    except Exception as e:
        pp(e)
        raise SystemExit
    _print(output)
    return output


def updateDefaultTimezone(tz):
    _print('Updating default timezone: {}'.format(tz))
    uids = execute('res.users', 'search', [[]], {
                   'context': {'active_test': False}})
    execute('res.users', 'write', [uids, {'tz': tz}])


def search_read(model, ids):
    ids_list = ids.split(',')
    if filter:
        _print('model {} with filter {}'.format(model, filter))
        execute(model, 'search_read', filter, kwargs)
    else:    
        _print('Fetching ids {} for model {}'.format(ids_list, model))
        execute(model, 'search_read', [[['id', 'in', ids_list]]], kwargs)


def setDefaultAccessRights():
    _print('Setting default access rights')
    config = execute('res.config.settings', 'create',
                     [{'user_default_rights': True}])
    execute('res.config.settings', 'execute', [config])


def activateLanguage(lang, setDefaultLang):
    _print('Activating language: {}'.format(lang))
    lang_id = execute('res.lang', 'search', [
                      [['active', '=', False], ['code', '=', lang]]])
    execute('res.lang', 'write', [lang_id, {'active': True}])

    lang_install_id = execute('base.language.install', 'create', [
                              {'lang': lang, 'overwrite': True}])
    execute('base.language.install', 'lang_install', [lang_install_id])

    update_translation_id = execute(
        'base.update.translations', 'create', [{'lang': lang}])
    execute('base.update.translations', 'act_update', [update_translation_id])

    if setDefaultLang:
        uids = execute('res.users', 'search', [[]], {
                       'context': {'active_test': False}})
        execute('res.users', 'write', [uids, {'lang': lang}])


if dar:
    setDefaultAccessRights()
if tz:
    updateDefaultTimezone(tz)
if lang:
    activateLanguage(lang, sdl)
if model:
    search_read(model, ids)
