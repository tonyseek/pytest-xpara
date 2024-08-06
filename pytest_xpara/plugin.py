import warnings

import py.path


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "xparametrize: mark test to run only on named environment"
    )


def pytest_addoption(parser):
    group = parser.getgroup('xpara', 'extended parametrizing plugin')
    group.addoption('--xpara', action='store_true', default=False,
                    help='Enable the extended parametrizing support. '
                         'default: False')


def pytest_generate_tests(metafunc):
    if not metafunc.config.option.xpara:
        return

    try:
        mark = getattr(metafunc.function, "xparametrize", None)
        if not mark:
            temp_mark = getattr(metafunc.function, "pytestmark", None)
            if temp_mark is not None:
                mark = next(iter(x for x in temp_mark if x.name == "xparametrize"), None)
            if not mark:
                return
        else:
            return
    except AttributeError:
        return
    else:
        xpara_data_name = (
            mark.args[0] if mark.args else metafunc.function.__name__)

    xpara_data = _load_data(metafunc, loaders=[
        _load_data_as_json,
        _load_data_as_yaml,
        _load_data_as_toml,
    ])
    item = xpara_data.get(xpara_data_name) if xpara_data else None
    if item:
        item_args = [
            arg.strip() for arg in item['args'].split(',') if arg.strip()]
        item_data = [
            [data.get(arg) for arg in item_args] for data in item['data']]
        metafunc.parametrize(item_args, item_data, ids=item.get('dataids'))


def _load_data(metafunc, loaders):
    data = getattr(metafunc.module, '__xpara_data__', None)
    if data is None:
        current_dir = py.path.local(metafunc.module.__file__).dirpath()
        file_name = metafunc.module.__name__.rsplit('.', 1)[-1]
        for loader in loaders:
            data = loader(current_dir, file_name)
            if data is not None:
                metafunc.module.__xpara_data__ = data
                break
    return data


IMPORT_TIPS = (
    'The fixture data file ("{0.basename}") exists but cannot be loaded because'
    ' of a lack of {1} parser, which could be installed by "pip install '
    '\'pytest-xpara[{2}]\'".')


def _load_data_as_json(current_dir, file_name):
    try:
        import simplejson as json
    except ImportError:
        import json

    data_file = current_dir.join('%s.json' % file_name)
    if not data_file.exists():
        return
    return json.loads(data_file.read())


def _load_data_as_yaml(current_dir, file_name):
    try:
        import yaml
    except ImportError:
        yaml = None

    for ext_name in ('yaml', 'yml'):
        data_file = current_dir.join('%s.%s' % (file_name, ext_name))
        if not data_file.exists():
            continue
        if yaml is None:
            warnings.warn(IMPORT_TIPS.format(data_file, 'YAML', 'yaml'))
            return
        return yaml.safe_load(data_file.read())


def _load_data_as_toml(current_dir, file_name):
    try:
        import toml
    except ImportError:
        toml = None

    data_file = current_dir.join('%s.toml' % file_name)
    if not data_file.exists():
        return
    if toml is None:
        warnings.warn(IMPORT_TIPS.format(data_file, 'TOML', 'toml'))
        return
    return toml.loads(data_file.read())
