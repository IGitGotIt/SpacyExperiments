"""
Setup script for MythoSciFi package.
"""

from setuptools import setup, find_packages

with open("README_PACKAGE.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mythoscifi",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Generate unique names by blending Greek mythology and sci-fi robot characters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mythoscifi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "chromadb>=1.3.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "kagglehub>=0.1.0",
        "pandas>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=5.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "mythoscifi-generate=mythoscifi.cli:generate_names",
            "mythoscifi-populate=mythoscifi.cli:populate_database",
            "mythoscifi-search=mythoscifi.cli:search_characters",
        ],
    },
)
