from setuptools import setup, find_packages

setup(
    name='hurwitz',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[],
    author='Harper Chisari',
    author_email='harper.chisari@harpresearch.ai',
    description='A module for working with Hurwitz quaternions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/HARP-research-Inc/hurwitz',  # URL to the project’s homepage
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
