from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "mycpp",
        [
            "src/app/pybind_api.cpp",
            "src/Utils.cpp",
        ],
        include_dirs=[
            "include",
            "/usr/local/include/eigen3",
            "/usr/include/eigen3",
            pybind11.get_include(),
        ],
        libraries=["boost_system", "boost_program_options"],
        language='c++',
        cxx_std=14,
        define_macros=[("VERSION_INFO", '"dev"')],
    ),
]

setup(
    name="mycpp",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
) 