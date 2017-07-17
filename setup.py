import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-appengine-toolbelt',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A django toolbelt for app engine projects',
    author='Rafael Braz',
    author_email='rafael@rbraz.com.br',
    url='www.rbraz.com.br',
)
