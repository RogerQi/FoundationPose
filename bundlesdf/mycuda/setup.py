# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import os, sys, torch, shutil, glob
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

code_dir = os.path.dirname(os.path.realpath(__file__))

# Get PyTorch library directory
torch_lib_dir = os.path.join(os.path.dirname(torch.__file__), 'lib')

# Find CUDA libraries
cuda_libs = []
if os.path.exists(torch_lib_dir):
    cuda_libs.extend(glob.glob(os.path.join(torch_lib_dir, 'libc10_cuda*.so*')))
    cuda_libs.extend(glob.glob(os.path.join(torch_lib_dir, 'libc10.so*')))
    cuda_libs.extend(glob.glob(os.path.join(torch_lib_dir, 'libtorch_cuda*.so*')))

nvcc_flags = ['-Xcompiler', '-O3', '-std=c++17', 
              '-U__CUDA_NO_HALF_OPERATORS__', 
              '-U__CUDA_NO_HALF_CONVERSIONS__', 
              '-U__CUDA_NO_HALF2_OPERATORS__']
c_flags = ['-O3', '-std=c++17']

# Set rpath to look in the same directory as the extension ($ORIGIN)
# and in a libs subdirectory within the package
linker_args = ['-Wl,-rpath,$ORIGIN', '-Wl,-rpath,$ORIGIN/libs']

class CustomBuildExt(BuildExtension):
    def run(self):
        # Run the normal build process
        super().run()
        
        # Create libs directory in the build directory
        if cuda_libs:
            # Find the build directory for our package
            build_lib = self.build_lib
            package_dir = os.path.join(build_lib, 'mycuda')
            libs_dir = os.path.join(package_dir, 'libs')
            
            # Create the libs directory
            os.makedirs(libs_dir, exist_ok=True)
            
            # Copy CUDA libraries to the libs directory
            for lib_path in cuda_libs:
                if os.path.exists(lib_path):
                    lib_name = os.path.basename(lib_path)
                    dest_path = os.path.join(libs_dir, lib_name)
                    print(f"Copying {lib_path} -> {dest_path}")
                    shutil.copy2(lib_path, dest_path)

# Prepare package data to include the libs directory
package_data = {'mycuda': ['libs/*']} if cuda_libs else {}

setup(
    name='foundationpose-mycuda',
    version='1.0.0',
    packages=['mycuda'],
    package_dir={'mycuda': '.'},
    package_data=package_data,
    ext_modules=[
        CUDAExtension('mycuda.common', [
            'bindings.cpp',
            'common.cu',
        ], 
        extra_compile_args={'gcc': c_flags, 'nvcc': nvcc_flags},
        extra_link_args=linker_args),
        CUDAExtension('mycuda.gridencoder', [
            f"{code_dir}/torch_ngp_grid_encoder/gridencoder.cu",
            f"{code_dir}/torch_ngp_grid_encoder/bindings.cpp",
        ], 
        extra_compile_args={'gcc': c_flags, 'nvcc': nvcc_flags},
        extra_link_args=linker_args),
    ],
    include_dirs=[
        "/usr/local/include/eigen3",
        "/usr/include/eigen3",
    ],
    cmdclass={'build_ext': CustomBuildExt},
    zip_safe=False,
    python_requires='>=3.7',
)