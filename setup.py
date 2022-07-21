import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ABSQL",
    version="0.1.7",
    author="Chris Cardillo",
    author_email="cfcardillo23@gmail.com",
    description="A rendering engine for templated SQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chriscardillo/ABSQL",
    packages=setuptools.find_packages(),
    install_requires=[
        "colorama",
        "flatdict",
        "Jinja2",
        "pendulum",
        "PyYaml",
        "SQLAlchemy",
        "sql-metadata",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
