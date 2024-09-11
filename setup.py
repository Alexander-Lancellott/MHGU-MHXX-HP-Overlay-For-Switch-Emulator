from setuptools import setup, Extension, find_packages

scanmodule = Extension('scanmodule', sources=['modules/scanmodule.c'])

setup(
    name="MHGU-MHXX-HP-Overlay-For-Switch-Emulator",
    author="Alexander-Lancellott",
    author_email="alejandrov.lancellotti@gmail.com",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "ahk[binary]==1.8.0",
        "ahk-wmutil==0.1.0",
        "colorama==0.4.6",
        "PySide6==6.7.2",
        "Pymem==1.13.1",
        "cursor==1.3.5",
        "pywin32==306",
        "numpy",
        "cx_Freeze",
        "art==6.2",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["build = modules.build:main"],
    },
    ext_modules=[scanmodule]
)
