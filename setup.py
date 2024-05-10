from setuptools import setup, find_packages

setup(
    name='genotools_api',
    version='0.0.1',
    author='Dan Vitale',
    author_email='dan@datatecnica.com',
    description='A FastAPI implementation of GenoTools (pypi: the_real_genotools) ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dvitale199/genotools_api',
    packages=find_packages(),
    install_requires=[
        "fastapi==0.111.0",
        "pydantic==2.7.1",
        "setuptools==69.5.1",
        "the_real_genotools==1.2.2",
        "uvicorn==0.29.0"
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
