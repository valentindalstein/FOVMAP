
"""
This setup file assumes installation of requirements file already
proceeded
"""

from setuptools import setup, find_packages
import sys

min_py_version = (3, 9)

# prompt for setup
if sys.version_info < min_py_version:
    sys.exit(
        'FOVMAP only tested'
        'on Python {}.{} or higher'.format(*min_py_version))

long_description = """
FOVMAP is a Python package that allows to visualize, map 
and project the field of view of a fly onto a cone surface. 
The package is based on the work of the authors of the paper 
"A neural algorithm for the simulation of the visual field 
of the fruit fly" (Barnes et al., 2019). It uses the vector 
representation of the fly eye to project the different ommatidia 
onto the cone surface and assess cone induced deformation.
"""

setup(
    name="FOVMAP",  # Change this to your package name
    version="0.0.1",
    description="Fly Ommatidia Visualization, Mapping And Projection",
    long_description=long_description,
    packages=find_packages(),  # Automatically find all packages in your project
    include_package_data=True,
    author='Valentin Dalstein',
    author_email='dalstein.valentin@gmail.com',
)
