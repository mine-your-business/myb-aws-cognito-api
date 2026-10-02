"""setup.py: setuptools control."""

from setuptools import setup, find_packages

__version__ = '1.1.0'

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='myb-aws-cognito-api',
    author='Mine Your Business',
    author_email='mine.your.business.crypto@gmail.com',
    packages=find_packages(exclude=("tests",)),
    version=__version__,
    description='Python library for communicating with the AWS Cognito API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'boto3>=1.43.107',
        'requests>=2.34.2',
    ],
    url='https://github.com/mine-your-business/myb-aws-cognito-api',
    python_requires='>=3.11',
    zip_safe=False,
    license='GPL-3',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
