# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.

from setuptools import setup
import os, sys, torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import glob

code_dir = os.path.dirname(os.path.realpath(__file__))

# Get PyTorch library directory
torch_lib_dir = os.path.join(os.path.dirname(torch.__file__), 'lib')

nvcc_flags = ['-Xcompiler', '-O3', '-std=c++17', 
              '-U__CUDA_NO_HALF_OPERATORS__', 
              '-U__CUDA_NO_HALF_CONVERSIONS__', 
              '-U__CUDA_NO_HALF2_OPERATORS__']
c_flags = ['-O3', '-std=c++17']

# Add rpath to find bundled libraries
linker_args = ['-Wl,-rpath,$ORIGIN']
linker_args.extend([f'-Wl,-rpath,{torch_lib_dir}'])

setup(
    name='foundationpose-mycuda',
    version='1.0.0',
    ext_modules=[
        CUDAExtension('common', [
            'bindings.cpp',
            'common.cu',
        ], 
        extra_compile_args={'gcc': c_flags, 'nvcc': nvcc_flags},
        extra_link_args=linker_args),
        CUDAExtension('gridencoder', [
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
    cmdclass={'build_ext': BuildExtension},
    zip_safe=False,
)