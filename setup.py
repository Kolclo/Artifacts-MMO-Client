import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_file(fname) -> str:
    with open(fname, encoding='utf-8') as f:
        return f.read()


setuptools.setup(
    name="Artifacts-MMO-Client",
    version="1",
    author="kolclo",
    packages=setuptools.find_packages(),
    require_Wheel=True,
    author_email="secret@secret.com",
    description="Python API client to control the Artifacts MMO game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kolclo/Artifacts-MMO-Client",
    install_requires=[
        "requests==2.32.3", 
        "pytest==8.3.2",
        "pygame==2.6.0"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires=">=3.10",
)