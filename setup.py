from setuptools import setup
import re

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('YuniteAPI/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md') as f:
    readme = f.read()

setup(name='YuniteAPI',
      author='SylteA',
      version=version,
      packages=['YuniteAPI'],
      license='MIT',
      description='A asynchronous python wrapper for the Yunite API',
      url='https://github.com/SylteA/YuniteAPI',
      long_description=readme,
      install_requires=requirements,
      python_requires='>=3.7.5',
      keywords=['wrapper', 'Yunite', 'api'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ])
