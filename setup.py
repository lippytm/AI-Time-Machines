#!/usr/bin/env python3
"""
AI Time Machines - Advanced AI Agent and Educational Platform
Setup configuration for the comprehensive AI learning and agent system.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-time-machines",
    version="1.0.0",
    author="AI Time Machines Team",
    description="Comprehensive AI Agent Platform with Educational Resources and Autonomous Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "requests>=2.25.0",
        "pyyaml>=5.4.0",
        "asyncio>=3.4.3",
        "aiohttp>=3.8.0",
        "sqlalchemy>=1.4.0",
        "psutil>=5.8.0",
        "scikit-learn>=1.0.0",
        "networkx>=2.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-asyncio>=0.21.0",
            "black>=21.9b0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "coverage>=6.0",
        ],
        "blockchain": [
            "web3>=5.24.0",
            "eth-account>=0.5.6",
            "cryptography>=3.4.0",
        ],
        "ml": [
            "tensorflow>=2.8.0",
            "torch>=1.11.0",
            "transformers>=4.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-time-machines=ai_time_machines.cli:main",
            "ai-agents=ai_time_machines.agents.cli:main",
            "ai-education=ai_time_machines.education.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/lippytm/AI-Time-Machines/issues",
        "Source": "https://github.com/lippytm/AI-Time-Machines",
    },
)