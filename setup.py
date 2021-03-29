from setuptools import setup
from pathlib import Path
from Cython.Build import cythonize

setup(
    long_description=Path('README.md').read_text(encoding='utf8'),
    long_description_content_type='text/markdown',
    install_requires=[
        "pygame>=2.0.1",
    ],
    ext_modules=cythonize(
        "pyfxr.pyx",
        compiler_directives={'embedsignature': True}
    ),
    zip_safe=False,
)
