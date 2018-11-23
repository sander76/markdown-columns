import os
import sys
from shutil import rmtree

from setuptools import setup, Command

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(
            "{0} setup.py sdist bdist_wheel --universal".format(sys.executable)
        )

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        # self.status("Pushing git tags…")
        # os.system("git tag v{0}".format(about["__version__"]))
        # os.system("git push --tags")

        sys.exit()


setup(
    name="markdown-columns",
    version="1.0.0",
    packages=["md_columns"],
    url="https://github.com/sander76/markdown-columns",
    license="MIT",
    author="Sander Teunissen",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    author_email="",
    description="css columns for Python Markdown",
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
