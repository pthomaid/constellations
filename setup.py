from setuptools import setup


def readme():
    with open('README.txt') as f:
        return f.read()

setup(
    name='constellations',
    version='0.0.1',
    author='Panagiotis Thomaidis',
    author_email='pthomaid@gmail.com',
    url='https://github.com/pthomaid/constellations',
    packages=['constellations', 'constellations.basics'],
    download_url = 'https://github.com/pthomaid/constellations',
    keywords = ['distributed', 'sockets'],
    description='Distributed multi-agent framework',
    long_description=readme(),
    classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Distributed Computing',
        ],
    test_suite="test"
)
