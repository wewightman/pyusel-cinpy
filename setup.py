from setuptools import Extension, setup

# load the C extentsion library
types = Extension(
    name="cinpy.types.__types__",
    include_dirs=["cinpy/types"],
    depends=["cinpy/types/cinpy.h"],
    sources=["cinpy/types/cinpy.c"]
)

# run setup tools
setup(
    name='pyusel-cinpy',
    description="C-Backed vectors and matrices",
    author_email="wew12@duke.edu",
    packages=['cinpy', 'cinpy.types'],
    package_dir={
        'cinpy':'cinpy', 
        'cinpy.types':'cinpy/types',
    },
    license="MIT",
    ext_modules=[types],
    install_requires=[
        "numpy",
    ],
    version="0.0.0"
)