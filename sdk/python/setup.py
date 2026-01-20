"""
Setup file for lippytm-ai-sdk Python package
Python equivalent to @lippytm/ai-sdk (Node)
"""

from setuptools import setup, find_packages

setup(
    name='lippytm-ai-sdk',
    version='1.0.0',
    description='AI/Web3 Integration SDK for AI Time Machines',
    author='',
    license='GPL-3.0',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[],
    extras_require={
        'ai': [
            'openai>=1.6.0',
            'transformers>=4.48.0',
            'huggingface-hub>=0.20.0',
            'langchain>=0.1.0',
            'llama-index>=0.9.0',
        ],
        'vector': [
            'pinecone-client>=3.0.0',
            'weaviate-client>=3.25.0',
            'chromadb>=0.4.0',
        ],
        'web3': [
            'web3>=6.13.0',
            'solana>=0.30.0',
            'eth-account>=0.10.0',
        ],
        'messaging': [
            'slack-sdk>=3.26.0',
            'discord.py>=2.3.0',
        ],
        'data': [
            'asyncpg>=0.29.0',
            'redis>=5.0.0',
            'boto3>=1.34.0',
            'ipfshttpclient>=0.8.0',
        ],
        'all': [
            'openai>=1.6.0',
            'transformers>=4.48.0',
            'huggingface-hub>=0.20.0',
            'langchain>=0.1.0',
            'llama-index>=0.9.0',
            'pinecone-client>=3.0.0',
            'weaviate-client>=3.25.0',
            'chromadb>=0.4.0',
            'web3>=6.13.0',
            'solana>=0.30.0',
            'eth-account>=0.10.0',
            'slack-sdk>=3.26.0',
            'discord.py>=2.3.0',
            'asyncpg>=0.29.0',
            'redis>=5.0.0',
            'boto3>=1.34.0',
            'ipfshttpclient>=0.8.0',
        ],
    },
    keywords=[
        'ai', 'web3', 'openai', 'huggingface', 'ethereum', 'solana',
        'vector-store', 'pinecone', 'weaviate', 'chroma'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
