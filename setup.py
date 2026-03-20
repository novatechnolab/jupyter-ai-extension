"""
Setup configuration for Jupyter AI Extension
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jupyter-ai-extension",
    version="1.0.0",
    author="Nova Technolab",
    author_email="contact@novatechnolab.com",
    description="Multi-LLM support for Jupyter Notebook (OpenAI, Claude, Gemini)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/novatechnolab/jupyter-ai-extension",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Jupyter",
    ],
    python_requires=">=3.8",
    install_requires=[
        "jupyter>=1.0.0",
        "ipython>=7.0.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "google-generativeai>=0.3.0",
        "requests>=2.28.0",
    ],
    keywords="jupyter notebook ai llm openai claude gemini",
    project_urls={
        "Bug Reports": "https://github.com/novatechnolab/jupyter-ai-extension/issues",
        "Source": "https://github.com/novatechnolab/jupyter-ai-extension",
        "License": "https://github.com/novatechnolab/jupyter-ai-extension/blob/main/LICENSE",
    },
)
