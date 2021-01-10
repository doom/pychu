import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

requirements = [
    "pydantic~=1.7.3",
]

yaml_requirements = [
    "PyYAML~=5.3.1",
]

toml_requirements = [
    "toml~=0.10.2",
]

setuptools.setup(
    name="pychu",
    version="1.0.0",
    author="Clément Doumergue",
    author_email="clement.doumergue@etna.io",
    description="Layered configuration powered by Pydantic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doom/pychu",
    packages=setuptools.find_namespace_packages(include=["pychu"]),
    install_requires=requirements,
    extras_require={
        "yaml": yaml_requirements,
        "toml": toml_requirements,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
