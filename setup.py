import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cisco_sdk",
    version="0.0.7",
    author="ali aqrabawi",
    author_email="ali_aqrabawi@yahoo.com",
    description="cisco devices SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ali-aqrabawi/cisco_sdk",
    packages=setuptools.find_packages(),

    install_requires=['easysnmp', 'jinja2', 'netmiko'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
