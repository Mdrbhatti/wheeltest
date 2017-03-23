from setuptools import setup, find_packages
setup(
    name='awesomegopy',
    version='0.0.1',
    description='Awesome.go in Python',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    data_files=[('lib', ['lib/awesome.so', 'lib/awesome.go', 'lib/awesome.h'])],
)