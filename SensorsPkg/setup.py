import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "Autonomous_Robot_Sensors", # change username if necessary
    version = "0.0.3",
    author = "Gabriel Casciano",
    author_email = "gabecasciano@gmail.com",
    description = "Sensor libraries for basic autonomous robot",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/GabeCasciano/Capstone20",
    project_urls = {
        "Bug Tracker" : "https://github.com/GabeCasciano/Capstone20/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux"
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    license="MIT"
)