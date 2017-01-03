from setuptools import setup, find_packages

with open('README.rst') as readme:
    next(readme)
    long_description = ''.join(readme).strip()

setup(
    name='pytest-xpara',
    version='0.1.0',
    description='An extended parametrizing plugin of pytest.',
    url='https://github.com/tonyseek/pytest-xpara',
    long_description=long_description,
    keywords=['pytest', 'parametrize', 'yaml'],
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    platforms=['any'],
    install_requires=[
        'pytest',
    ],
    extras_require={
        'yaml': ['PyYAML'],
        'toml': ['toml'],
    },
    entry_points={
        'pytest11': [
            'xpara = pytest_xpara.plugin',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
