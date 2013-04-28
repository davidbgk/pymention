from setuptools import setup, find_packages

version = '0.1'

LONG_DESCRIPTION = """
Using pymention
===============

This is a very alpha stage of the development of the WebMention spec.

Only recommended for hacking :-).
"""

setup(
    name='pymention',
    version=version,
    description="pymention",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    keywords='webmention,wsgi',
    author='David Larlet',
    author_email='larlet@gmail.com',
    url='http://github.com/davidbgk/pymention/',
    license='BSD',
    packages=find_packages(),
    package_data={
        'pymention': [
            'pymention/*.py',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
