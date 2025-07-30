from setuptools import setup
from pathlib import Path
from Cython.Build import cythonize

setup(
    long_description=Path('README.md').read_text(encoding='utf8'),
    long_description_content_type='text/markdown',
    extras_require={
        'gui': [
            "pygame>=2.0.1",
        ]
    },
    packages=['pyfxr'],
    package_data={
        'pyfxr': ['py.typed', '_pyfxr.pyi']
    },
    entry_points={
        'console_scripts': [
            'pyfxr = pyfxr.gui:main [gui]',
        ]
    },
    ext_modules=cythonize(
        "pyfxr/_pyfxr.pyx",
        compiler_directives={'embedsignature': True}
    ),
    zip_safe=False,
)
