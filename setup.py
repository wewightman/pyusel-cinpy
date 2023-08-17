from setuptools import Extension, setup

# load the C extentsion library
types = Extension(
    name="cinpy.conversions.__conversions__",
    include_dirs=["cinpy/conversions"],
    depends=["cinpy/conversions/cinpy.h"],
    sources=["cinpy/conversions/cinpy.c"]
)

# run setup tools
setup(
    name='pyusel-cinpy',
    description="C-Backed vectors and matrices",
    author_email="wew12@duke.edu",
    packages=['cinpy', 'cinpy.conversions'],
    package_dir={
        'cinpy':'cinpy', 
        'cinpy.conversions':'cinpy/conversions',
    },
    license="MIT",
    ext_modules=[types],
    install_requires=[
        "numpy",
    ],
    version="0.0.0"
)