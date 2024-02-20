from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="groqccoli",
    version="0.1.0",
    description="An unoffical Python client for Groq's inference API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0x7B5/Groqccoli",
    packages=find_packages(),
    requires=["requests"],
)
