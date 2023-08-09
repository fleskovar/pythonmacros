from setuptools import setup

files = ["config.json"]

setup(
    name="pythonmacros",
    version="0.1.0",
    packages=["pythonmacros"],
    entry_points={
        "console_scripts": [
            "pythonmacros = pythonmacros.__main__:main"
        ]
    },
    package_data = {'package' : files },
    install_requires=[
        'pynput',
      ],
)