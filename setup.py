import setuptools

with open("README.md", "r") as ld:
    long_description = ld.read()

setuptools.setup(
    name="asprilo-mapfconverter",
    version="0.1.1",
    author="Wassily Korth",
    author_email="wkorth@uni-potsdam.de",
    description="A converter from movingai's formats to asprilo's",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wkorth/asprilo-mapfConverter",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': [
                           'map-to-lp = mapfconverter.map_to_lp:main',
                           'scen-to-lp = mapfconverter.scen_to_lp:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)