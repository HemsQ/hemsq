from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="hemsq",
    version="0.1.0",
    description="HEMS scheduling module using annealing machines",
    author="Yukino Terui, Canon Mukai",
    url="https://github.com/CanonMukai/hemsq-prototype.git",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt')
)
