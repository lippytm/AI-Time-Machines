from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-time-machines",
    version="0.1.0",
    author="AI Time Machines Team",
    description="Adding AI Agents to everything with Time Machines - Git cloning and web scraping capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lippytm/AI-Time-Machines",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "gitpython>=3.1.40",
        "lxml>=4.9.0",
        "selenium>=4.15.0",
        "urllib3>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-time-machines=ai_time_machines.cli:main",
        ],
    },
)