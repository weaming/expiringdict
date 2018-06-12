from setuptools import setup, find_packages
try:
    import md5  # fix for "No module named _md5" error
except ImportError:
    # python 3 moved md5
    from hashlib import md5

with open("README.rst") as f:
    long_description = f.read()


setup(name='expiringdict_with_default',
      version='1.1.7',
      description="Dictionary with auto-expiring values for caching purposes, support default value",
      long_description=long_description,
      author='weaming',
      author_email='garden.yuen@gmail.com',
      url='https://github.com/weaming/expiringdict',
      license='Apache 2',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True,
      extras_require={'test': ['nose', 'mock', 'coverage']})
