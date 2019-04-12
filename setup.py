from setuptools import setup, find_packages

__version__ = '0.1'


setup(
    name='bot',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'python-dotenv',
        'passlib'
    ],
    entry_points={
        'console_scripts': [
            'bot = bot.manage:cli'
        ]
    }
)
