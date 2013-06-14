from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='thrift_template',
      version=version,
      description="template to create thrift services",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='thrift paster',
      author='yancl',
      author_email='kmoving@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.paster_create_template]
      thrift_service = thrift_template.templates:ThriftServiceTemplate
      thrift_server  = thrift_template.templates:ThriftServerTemplate
      """,
      )
