import shutil

import pkg_resources
import setuptools
from setuptools.command.build_py import build_py

try:
    # Only needed if installing Rust extensions
    from setuptools_rust import Binding, RustExtension
except ImportError:
    pass


def install_ext_modules():
    swig_modules = []
    rust_modules = []

    swig_path = shutil.which('swig')
    if swig_path is not None:
        swig_modules = [
            setuptools.Extension(name='_seedow',
                                 sources=['lib/c/ext.c', 'lib/c/ext.i'])
        ]

    installed = {pkg.key for pkg in pkg_resources.working_set}
    if 'setuptools-rust' in installed:
        rust_modules = [RustExtension('seedow_rust', binding=Binding.PyO3)]

    return (swig_modules, rust_modules)


def run_setup(swig_modules, rust_modules):
    setuptools.setup(
        name='seedow',
        version='0.0.1',
        author=author,
        author_email=author_email,
        description='Scrape election data out of Wikipedia',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/ryw89/seedow',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
        ],
        install_requires=install_requires,
        python_requires='>=3.6',
        include_package_data=True,
        package_data={'': ['data/*.txt', 'data/*.csv']},
        entry_points=entry_points,
        ext_modules=swig_modules,
        rust_extensions=rust_modules,
        cmdclass={
            'build_py': BuildPy,
        },
    )

    if not swig_modules and not rust_modules:
        print('*' * 75)
        print(
            'WARNING: The extension modules were not compiled, speedups are not enabled.'
        )
        print('Plain-Python installation succeeded.')
        print('*' * 75)


class BuildPy(build_py):
    def run(self):
        # We need to be building our extension modules first, so we'll
        # alter the build_py class from setuptools
        self.run_command('build_ext')
        super(build_py, self).run()


with open('README.md', 'r') as f:
    long_description = f.read()

install_requires = [
    'beautifulsoup4', 'nltk', 'pandas', 'sklearn', 'tqdm', 'wikipedia',
    'wikitablescrape'
]

authors = {'Ryan Whittingham': 'ryanwhittingham89@gmail.com'}

author = ', '.join(list(authors.keys()))
author_email = ', '.join(list(authors.values()))

entry_points = {
    'console_scripts': [
        'seedow-wordcounts=seedow.goodies.__main__:main',
        'seedow-templatelinks=seedow.scrapers.__main__:templates',
    ]
}

swig_modules, rust_modules = install_ext_modules()
run_setup(swig_modules, rust_modules)
