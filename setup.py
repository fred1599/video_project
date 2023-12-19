from setuptools import setup

setup(
    name="VotreProjet",
    version="1.0",
    packages=["video"],
    entry_points={"console_scripts": ["video=video.__main__:app"]},
)
