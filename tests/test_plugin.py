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

        def test_baz():
            assert 1 + 1 == 2
    ''')
    testdir.makefile('.py', test_baz='''
        def test_baz():
            assert 1 + 1 == 2
    ''')
    result = testdir.runpytest_subprocess('--verbose', '--xpara')
    result.assert_outcomes(passed=5, skipped=0, failed=1)
    result.stdout.fnmatch_lines_random(r'''
        test_foobar.py::test_foo*13-15* PASSED
        test_foobar.py::test_foo*15-16* FAILED
        test_foobar.py::test_bar*13-14* PASSED
        test_foobar.py::test_bar*15-16* PASSED
        test_foobar.py::test_baz PASSED
    ''')


@parametrize_data
def test_run_without_default_name(testdir, data_ext, data_content):
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
    # result.assert_outcomes(passed=0, skipped=0, failed=1)
    result.stdout.fnmatch_lines_random(r'''
        E * fixture 'foo' not found
    ''')
