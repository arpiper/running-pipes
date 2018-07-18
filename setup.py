from setuptools import find_packages, setup

with open('README.md', 'r') as rdme:
    long_description = rdme.read()

setup(
    name='Running Pipes',
    version='0.1.0',
    author='Andrew Piper',
    description='small web app to track running goals',
    long_description=long_desciption,
    long_description_type='text/markdown',
    packages=find_packages(),
    include_package_data=True, # this includes static/template dirs
    zip_safe=False,
    install_requires=[
        'rungoals',
    ],
)
