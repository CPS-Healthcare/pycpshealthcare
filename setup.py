from setuptools import find_packages, setup

setup(
    name="pycpshealthcare",
    packages=find_packages(),
    version="2.1.0",
    description="Python library for ANID ACT210083 project data collection and processing.",
    author="Fernando Huanca",
    license="MIT",
    setup_requires=["wheel"],
    install_requires=["pandas>=1.5,<=2", "pymongo>=4.0,<=5"],
    url="https://docs.cpshealthcare.cl/static/pycpshealthcare-html/index.html",
)
