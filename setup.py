from setuptools import setup
from setuptools import find_packages

setup(name='pimg',
      version='0.0.0.1',
      description='PNG Image Server',      
      packages=find_packages(),
      install_requires=[
          'flask',
          'PIL'
      ],
      zip_safe=False)