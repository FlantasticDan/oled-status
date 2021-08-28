import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oled-status",
    version="0.0.1",
    author="Daniel Flanagan",
    description="Status message logger for embedded systems equipped with a small OLED display.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FlantasticDan/oled-status",
    project_urls={
        "Bug Tracker": "https://github.com/FlantasticDan/oled-status/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=['httpx'],
    extra_requires={
        "server": ['adafruit-circuitpython-ssd1306', 'Pillow', 'flask', 'gevent'],
        "draw": ['Pillow']
    },
    package_data={
        "": ["*.tff"]
    }
)