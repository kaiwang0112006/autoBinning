import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoBinning",
    version="0.1.4",
    author="Kai Wang",
    author_email="wangkai0112006@163.com",
    description="A small package for feature autoBinning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaiwang0112006/autoBinning",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
