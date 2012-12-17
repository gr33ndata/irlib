from distutils.core import setup

setup(
	name='IRLib',
	version='0.1.0',
	author='Tarek Amr',
	author_email='',
	packages=['irlib'],
	scripts=['bin/classify.py'],
	url='http://pypi.python.org/pypi/IRLib/',
	license='LICENSE.txt',
	description='Inforamtion Retrieval Library',
	long_description=open('README.md').read(),
)
