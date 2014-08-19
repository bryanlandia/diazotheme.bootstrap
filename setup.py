from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='yes.diazotheme',
      version=version,
      description="Plone theme based on Twitter's Bootstrap CSS",
      long_description=open("README.rst").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='plone diazo theme',
      author='Bryan Wilson (based on diazotheme.bootstrap by Izhar Firdaus)',
      author_email='bryanlandia@gmail.com',
      url='http://yesmagazine.org',
      license='Apache License 2.0',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['yes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
