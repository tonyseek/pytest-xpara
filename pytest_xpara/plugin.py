from __future__ import absolute_import

import yaml
import py.path


def pytest_addoption(parser):
    group = parser.getgroup('xpara', 'extended parametrizing plugin')
    group.addoption('--xpara', action='store_true', default=False,
                    help='Enable the extended parametrizing support. '
                    'default: False')


def pytest_generate_tests(metafunc):
    if not metafunc.config.option.xpara:
        return

    xpara_data = getattr(metafunc.module, '__xpara_data__', None)
    if xpara_data is None:
        current_dir = py.path.local(metafunc.module.__file__).dirpath()
        xpara_data_name = metafunc.module.__name__.rsplit('.', 1)[-1]
        xpara_data_file = current_dir.join('%s.yaml' % xpara_data_name)
        if not xpara_data_file.exists():
            return
        xpara_data = yaml.load(xpara_data_file.read())
        metafunc.module.__xpara_data__ = xpara_data

    try:
        mark = metafunc.function.parametrize_from_yaml
    except AttributeError:
        return
    else:
        xpara_data_name = (
            mark.args[0] if mark.args else metafunc.function.__name__)

    item = xpara_data.get(xpara_data_name)
    if item:
        item_args = item['args'].split(',')
        item_data = [
            [data.get(arg) for arg in item_args] for data in item['data']]
        metafunc.parametrize(item['args'], item_data, ids=item.get('dataids'))
