import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sciapp_toolkit",
    version="0.0.dev1",
    author="Ross Barnowski",
    author_email="rossbar@berkeley.edu",
    description=("Toolkit for building native desktop applications for "
                 "real-time acquisition and analysis of data from scientific "
                 "instruments."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rossbar/sciapp_toolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)
