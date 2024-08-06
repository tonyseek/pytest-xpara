|Build Status| |Coverage Status| |PyPI Version|

pytest-xpara
============

*pytest-xpara* is an extended parametrizing plugin of pytest.


Installation
------------

::

    pip install pytest-xpara


Usage
-----

::

    py.test --xpara test_foo.py


Example
-------

.. code-block:: python

    # test_foo.py
    import pytest

    @pytest.mark.xparametrize
    def test_bar(lhs, rhs):
        assert lhs == -rhs

.. code-block:: yaml

    # test_foo.yaml
    test_bar:
      args: lhs,rhs
      data:
        - lhs: 1
          rhs: -1
        - lhs: -1
          rhs: 1
      dataids:
        - left_to_right
        - right_to_left

::

    $ py.test -v --xpara test_foo.py
    ========================== test session starts ===========================
    platform darwin -- Python 2.7.12, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
    cachedir: ../.cache
    rootdir: /Users/tonyseek/Sites/pytest-xpara, inifile: setup.cfg
    plugins: xpara-0.0.0, cov-2.4.0
    collecting ... collected 2 items

    test_foo.py::test_bar[left_to_right] PASSED
    test_foo.py::test_bar[right_to_left] PASSED

    ======================== 2 passed in 0.03 seconds ========================


Contributing
------------

If you want to report bugs or request features, please feel free to open issues
or create pull requests on GitHub_.


.. _GitHub: https://github.com/tonyseek/pytest-xpara/issues
.. |Build Status| image:: https://img.shields.io/github/actions/workflow/status/tonyseek/pytest-xpara/check.yml?branch=master&style=flat
   :target: https://github.com/tonyseek/pytest-xpara/actions/workflows/check.yml
   :alt: Build Status
.. |Coverage Status| image:: https://img.shields.io/coverallsCoverage/github/tonyseek/pytest-xpara?style=flat&branch=master
   :target: https://coveralls.io/github/tonyseek/pytest-xpara
   :alt: Coverage Status
.. |PyPI Version| image:: https://img.shields.io/pypi/v/pytest-xpara?style=flat
   :target: https://pypi.org/project/pytest-xpara/
   :alt: PyPI Version
