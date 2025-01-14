#!/usr/bin/env python
# Copyright (C) Alibaba Group Holding Limited. All rights reserved.
import glob
import re
from os import path

import setuptools
import torch
from torch.utils.cpp_extension import CppExtension

torch_ver = [int(x) for x in torch.__version__.split('.')[:2]]
assert torch_ver >= [1, 7], 'Requires PyTorch >= 1.7'


def get_extensions():
    this_dir = path.dirname(path.abspath(__file__))
    extensions_dir = path.join(this_dir, 'damo', 'layers', 'csrc')

    main_source = path.join(extensions_dir, 'vision.cpp')
    sources = glob.glob(path.join(extensions_dir, '**', '*.cpp'))

    sources = [main_source] + sources
    extension = CppExtension

    extra_compile_args = {'cxx': ['-O3']}
    define_macros = []

    include_dirs = [extensions_dir]

    ext_modules = [
        extension(
            'damo._C',
            sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
        )
    ]

    return ext_modules


with open('damo/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(),
                        re.MULTILINE).group(1)

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='damo',
    version=version,
    author='basedet team',
    python_requires='>=3.6',
    long_description=long_description,
    ext_modules=get_extensions(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    cmdclass={'build_ext': torch.utils.cpp_extension.BuildExtension},
    packages=setuptools.find_packages(),
)
