from setuptools import setup, find_packages

setup(
    name='giso',
    version='0.1.0',
    author='Claudio Paladini',
    author_email='claudio.paladini@bath.edu',
    description='A simple interace for basic GIS operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/paladinic/giso',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
