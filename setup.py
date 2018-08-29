import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cscmiko",
    version="0.0.1",
    author="ali aqrabawi",
    author_email="ali_aqrabawi@yahoo.com",
    description="cisco devices SDK based on netmiko",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ali-aqrabawi/cscmiko",
    packages=setuptools.find_packages(),

    install_requires=['jinja2', 'netmiko'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
