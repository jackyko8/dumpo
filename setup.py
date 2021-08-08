import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dumpo",
    version="0.0.7",
    author="Jacky Ko",
    author_email="jko@accsoft.com.au",
    description="Dumpo Python Object Serialiser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackyko8/dumpo",
    project_urls={
        "Bug Tracker": "https://github.com/jackyko8/dumpo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
