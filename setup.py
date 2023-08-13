from setuptools import setup, find_packages

setup(
    name='plexport',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'plexport = app.cli:cli_entry',
        ],
    },
    install_requires=[
        "plexapi", "coloredlogs"
    ],
)
