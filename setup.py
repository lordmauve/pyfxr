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
    py_modules=['pyfxr', 'pyfxr_gui'],
    entry_points={
        'console_scripts': [
            'pyfxr = pyfxr_gui:main [gui]',
        ]
    },
    ext_modules=cythonize(
        "_pyfxr.pyx",
        compiler_directives={'embedsignature': True}
    ),
    zip_safe=False,
)
