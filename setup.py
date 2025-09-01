#!/usr/bin/env python3
"""
AI-Time-Machines: Adding AI Agents to everything with Time Machines
Setup script for package installation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-time-machines",
    version="0.1.0",
    author="AI-Time-Machines Team",
    description="Adding AI Agents to everything with Time Machines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lippytm/AI-Time-Machines",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "pydantic>=1.10.0",
        "python-dotenv>=0.19.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "web3": [
            "web3>=6.0.0",
            "eth-account>=0.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-time-machines=ai_time_machines.cli:main",
        ],
    },
)