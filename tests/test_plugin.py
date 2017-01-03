from __future__ import absolute_import


pytest_plugins = 'pytester'


def test_run(testdir):
    testdir.makefile('.yaml', test_foobar='''
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
    ''')
    testdir.makefile('.py', test_foobar='''
        import pytest

        @pytest.mark.parametrize_from_yaml
        def test_foo(foo, bar):
            assert foo + 2 == bar

        @pytest.mark.parametrize_from_yaml
        def test_bar(foo, bar):
            assert foo + 1 == bar

        def test_baz():
            assert 1 + 1 == 2
    ''')
    result = testdir.runpytest_subprocess('--verbose', '--xpara')
    result.assert_outcomes(passed=4, skipped=0, failed=1)
    result.stdout.fnmatch_lines_random(r'''
        test_foobar.py::test_foo*13-15* PASSED
        test_foobar.py::test_foo*15-16* FAILED
        test_foobar.py::test_bar*13-14* PASSED
        test_foobar.py::test_bar*15-16* PASSED
        test_foobar.py::test_baz PASSED
    ''')


def test_run_disabled(testdir):
    testdir.makefile('.py', test_foobar='''
        import pytest

        @pytest.mark.parametrize_from_yaml
        def test_foo(foo, bar):
            assert foo + 2 == bar
    ''')
    result = testdir.runpytest_subprocess('--verbose')
    # result.assert_outcomes(passed=0, skipped=0, failed=1)
    result.stdout.fnmatch_lines_random(r'''
        E * fixture 'foo' not found
    ''')
