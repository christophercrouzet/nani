import io
import os
import re
import setuptools


def _read(*names, **kwargs):
    # Credits: https://packaging.python.org/single_source_version.
    here = os.path.dirname(__file__)
    encoding = kwargs.get('encoding', 'utf8')
    with io.open(os.path.join(here, *names), encoding=encoding) as fp:
        return fp.read()


def _find_version(*file_paths):
    # Credits: https://packaging.python.org/single_source_version.
    version_file = _read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find the version string.")


setuptools.setup(
    name='nani',
    version=_find_version('nani.py'),
    description="Alternative approach to defining and viewing NumPy's arrays",
    long_description=_read('README.rst'),
    keywords='nani numpy dtype view',
    license='MIT',
    url='https://github.com/christophercrouzet/nani',
    author="Christopher Crouzet",
    author_email='christopher.crouzet@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=['numpy'],
    extras_require={
        'dev': ['coverage', 'pycodestyle', 'pydocstyle', 'pylint',
                'sphinx>=1.3', 'tox'],
        'docs': ['sphinx>=1.3'],
    },
    packages=[],
    py_modules=['nani'],
    include_package_data=True
)
