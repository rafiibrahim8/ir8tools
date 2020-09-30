from setuptools import setup,find_packages
from ir8tools import __version__

def read_file(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            return f.read()
    except:
        return []

requirements = read_file('requirements.txt')
long_description = read_file('README.md')
tools = read_file('tool_descriptions.txt').strip().split()

setup(
    name='ir8tools',
    version=__version__,
    
    author='Ibrahim Rafi',
    author_email='me@ibrahimrafi.me',

    license='MIT',

    url='https://github.com/rafiibrahim8/ir8tools',
    download_url = 'https://github.com/rafiibrahim8/ir8tools/archive/v{}.tar.gz'.format(__version__),

    install_requires=requirements,

    description='Download files from google drive with resuming capability.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['scripts', 'tools'],

    packages=find_packages(),
    entry_points=dict(
        console_scripts=tools
    ),

    platforms=['any'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
