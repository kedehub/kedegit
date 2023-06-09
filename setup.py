import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='kedehub',
    version='0.1.0',
    author='MMI',
    author_email='support@kedehub.com',
    description='KEDE analyzer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://kedehub.com',
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.8',
    install_requires=[
        'gitpython',
        'python-dateutil',
        'beautifultable'
    ]
)
