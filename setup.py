from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="termi-cheat",
    version="1.0.0",
    description="Termi-Cheat - Cheatsheets de comandos para terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/termi-cheat",
    author="Tu Nombre",
    author_email="tu.email@ejemplo.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    keywords="cheatsheet, terminal, commands, reference",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0"],
    },
    entry_points={
        "console_scripts": [
            "termi-cheat=termi_cheat.cli:main",
            "tcheat=termi_cheat.cli:main",  # Short alias
        ],
    },
    package_data={
        "termi_cheat": ["cheats/*.json"],
    },
    project_urls={
        "Bug Reports": "https://github.com/tuusuario/termi-cheat/issues",
        "Source": "https://github.com/tuusuario/termi-cheat",
    },
)