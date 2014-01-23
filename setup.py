from setuptools import setup, find_packages


setup(
    name='lolcommits_server',
    version='0.1',
    description="Dat commit face.",
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    tests_require='nose',
    test_suite='nose.collector',
)
