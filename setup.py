from distutils.core import setup

setup(
    name='frontik',
    version='2.7.4dev',

    package_dir = {'': 'src'},
    packages = ['frontik'],

    scripts = ['src/frontik_srv.py']
)
