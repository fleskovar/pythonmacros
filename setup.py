from setuptools import setup, find_packages

files = ["config.json"]

setup(
    name="pythonmacros",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pythonmacros = pythonmacros.__main__:main"
        ]
    },
    package_data = {'pythonmacros' : files },
    install_requires=[
        "pynput",
        "pyautogui"
      ],
)