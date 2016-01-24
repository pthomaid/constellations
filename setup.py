from setuptools import setup

# Note: setuptools are not part of the python installation, 
# need to install separately, using pip for example, befor running this setup

def readme():
    with open('README.txt') as f:
        return f.read()	

setup(
    name='constellations',
    version='0.0.2',
    author='Panagiotis Thomaidis',
    author_email='pthomaid@gmail.com',
    url='https://github.com/pthomaid/constellations',
    packages=['constellations'],
    download_url = 'https://github.com/pthomaid/constellations',
    keywords = ['distributed', 'gossip'],
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
    test_suite="tests"
)
