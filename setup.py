# Standard Library
import os
import subprocess

# Third Party Stuff

# from pip.req import parse_requirements
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    
from setuptools import find_packages, setup
from setuptools.command.install import install as InstallCommand
from setuptools.command.test import test as TestCommand

here = os.path.dirname(__file__)

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(
    os.path.join(here, 'requirements.txt',),
    session=0,
)

try:
    # newest versions.
    # pip>=21.x.x
    from pip._internal.req.constructors import (
        install_req_from_parsed_requirement,
    )
except ImportError:
    # pip<=20.x.x
    def install_req_from_parsed_requirement(x):
        return x

# for pip==21.x.x convert ParsedRequirement into InstallRequirement.
install_reqs = [install_req_from_parsed_requirement(req) for req in install_reqs]

install_requires = [str(ir.req) for ir in install_reqs]


def read(fname):
    return open(os.path.join(here, fname)).read()


class NoseTestCommand(TestCommand):
    # Inspired by the example at https://pytest.org/latest/goodpractises.html

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])


class CustomInstallCommand(InstallCommand):
    def run(self, *args, **kwargs):
        # Copy html2latex_webkit2png.py script
        p = subprocess.Popen(["sudo", "cp", os.path.join(here, "scripts/html2latex_webkit2png.py"), "/usr/local/bin/html2latex_webkit2png.py"])
        p.wait()

        p = subprocess.Popen(["sudo", "chmod", "+x", "/usr/local/bin/html2latex_webkit2png.py"])
        p.wait()

        # Run `bower install`
        p = subprocess.Popen(["bower", "install"])
        p.wait()

        return InstallCommand.run(self, *args, **kwargs)


setup(
    name="html2latex",
    version="0.0.62",
    author="Pankaj Singh",
    author_email="pankaj@xamcheck.com",
    description=("Convert HTML to latex."),
    license="BSD",
    keywords="html, latex",
    url="https://github.com/psjinx/html2latex",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages('src'),
    package_dir={
        '': 'src',
    },
    namespace_packages=['html2latex'],
    install_requires=install_requires,
    cmdclass={
        'install': CustomInstallCommand,
        'test': NoseTestCommand,
    },
    test_suite = "nose.collector",
    include_package_data=True,
    zip_safe=False,
)
