from distutils.core import setup

setup(
	name='UEA-IRLib',
	version='0.1.0',
	author='Tarek Amr',
	author_email='t.amr@uea.ac.uk',
	packages=['irlib'],
	scripts=['bin/classify.py'],
	url='http://pypi.python.org/pypi/IRLib/',
	license='LICENSE.txt',
	description='',
	long_description=open('README.txt').read(),
	install_requires=[
		"Django >= 1.1.1",
		"caldav == 0.1.4",
	],
)
