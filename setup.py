import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

setup(
    name="skinpy",
    version="0.0.2",
    description="",
    long_description=long_description,
    license="LGPL v3",
    url="http://github.com/jackuess/skinpy",

    author="Jacques de Laval",
    author_email="jacques@tuttosport.se",

    packages=["skinpy"],

    install_requires=["console_colors"],
    tests_require=["nose", "mock"],
    test_suite="nose.collector",
    extras_require={
        "docs": ["sphinx"]
    }
)
