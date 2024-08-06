from __future__ import absolute_import

import pytest

pytest_plugins = 'pytester'

# TODO hmm.. bootstrap in future
parametrize_data = pytest.mark.parametrize('data_ext,data_content', [
    ('.json', '''
        {
            "test_foo": {
                "args": "foo,bar",
                "data": [
                    {"foo": 13, "bar": 15},
                    {"foo": 15, "bar": 16}
                ]
            },
            "test_bar": {
                "args": "foo,bar",
                "data": [
                    {"foo": 13, "bar": 14},
                    {"foo": 15, "bar": 16}
                ]
            },
            "test_one_parameter": {
                "args": "foo",
                "data": [
                    {"foo": 15},
                    {"foo": "16"}
                ]
            }
        }
    '''),
    ('.yaml', '''
        test_foo:
          args: foo,bar
          data:
            - foo: 13
              bar: 15
            - foo: 15
              bar: 16

        test_bar:
          args: foo,bar
          data:
            - foo: 13
              bar: 14
            - foo: 15
              bar: 16

        test_one_parameter:
          args: foo
          data:
            - foo: 15
            - foo: "16"
    '''),
    ('.toml', '''
        [test_foo]
        args = "foo,bar"
          [[test_foo.data]]
          foo = 13
          bar = 15
          [[test_foo.data]]
          foo = 15
          bar = 16

        [test_bar]
        args = "foo,bar"
          [[test_bar.data]]
          foo = 13
          bar = 14
          [[test_bar.data]]
          foo = 15
          bar = 16

        [test_one_parameter]
        args = "foo"
          [[test_one_parameter.data]]
          foo = 15
          [[test_one_parameter.data]]
          foo = "16"
    '''),
], ids=['json', 'yaml', 'toml'])


@parametrize_data
def test_run(testdir, data_ext, data_content):
    testdir.makefile(data_ext, test_foobar=data_content)
    testdir.makefile('.py', test_foobar='''
        import pytest

        @pytest.mark.xparametrize
        def test_foo(foo, bar):
            assert foo + 2 == bar

        @pytest.mark.xparametrize
        def test_bar(foo, bar):
            assert foo + 1 == bar

        @pytest.mark.xparametrize
        def test_one_parameter(foo):
            assert isinstance(foo, int)

        def test_baz():
            assert 1 + 1 == 2
    ''')
    testdir.makefile('.py', test_baz='''
        def test_baz():
            assert 1 + 1 == 2
    ''')
    result = testdir.runpytest_subprocess('--verbose', '--xpara')
    result.assert_outcomes(passed=6, skipped=0, failed=2)
    result.stdout.re_match_lines_random(
        [
            r"^.*?test_foobar.py::test_foo\[13\-15\].*?PASSED.*?$",
            r"^.*?test_foobar.py::test_foo\[15\-16\].*?FAILED.*?$",
            r"^.*?test_foobar.py::test_bar\[13\-14\].*?PASSED.*?$",
            r"^.*?test_foobar.py::test_bar\[15\-16\].*?PASSED.*?$",
            r"^.*?test_foobar.py::test_one_parameter\[15\].*?PASSED.*?$",
            r"^.*?test_foobar.py::test_one_parameter\[16\].*?FAILED.*?$",
            r"^.*?test_foobar.py::test_baz.*?PASSED.*?$"
        ]
    )


@parametrize_data
def test_run_with_custom_name(testdir, data_ext, data_content):
    testdir.makefile(data_ext, test_foobar=data_content)
    testdir.makefile('.py', test_foobar='''
        import pytest

        @pytest.mark.xparametrize('test_bar')
        def test_boom(foo, bar):
            assert foo + 1 == bar
    ''')
    result = testdir.runpytest_subprocess('--xpara')
    result.assert_outcomes(passed=2, skipped=0, failed=0)


def test_run_disabled(testdir):
    testdir.makefile('.py', test_foobar='''
        import pytest

        @pytest.mark.xparametrize
        def test_foo(foo, bar):
            assert foo + 2 == bar
    ''')
    result = testdir.runpytest_subprocess('--verbose')
    result.stdout.re_match_lines_random(r"^.*?fixture 'foo' not found.*?$")


@pytest.mark.parametrize('ext_name,pkg_fullname,warning_pattern', [
    ('.yaml', 'yaml', r'.*YAML parser.+pytest-xpara\[yaml\].*'),
    ('.toml', 'toml', r'.*TOML parser.+pytest-xpara\[toml\].*'),
])
def test_run_without_parser(testdir, ext_name, pkg_fullname, warning_pattern):
    testdir.makefile(ext_name, test_foobar='')
    testdir.makefile('.py', test_foobar='''
        import pytest

        @pytest.mark.xparametrize
        def test_boom(foo, bar):
            assert foo + 3 == bar
    ''')
    testdir.makefile('.py', conftest='''
        import sys
        import pytest

        class MockMetaPathFinder:
            def find_spec(self, fullname, path, target=None):
                if fullname == '{0}':
                     raise ImportError('mock')

        def pytest_configure(config):
            sys.meta_path.insert(0, MockMetaPathFinder())
    '''.format(pkg_fullname))
    result = testdir.runpytest_subprocess('--xpara')
    result.stdout.re_match_lines_random(warning_pattern)
