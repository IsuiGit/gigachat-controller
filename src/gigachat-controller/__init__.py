[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "gigachat-controller"
version = "0.1.0"
description = "GigaChat Meta Controller and Audit System"
readme = "README.md"
authors = [
    {name = "Isui", email = "gitpusherisui@gmail.com"}
]
license = {text = "MIT"}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
requires-python = ">=3.11"
dependencies = [
    # список зависимостей, например:
    # "requests>=2.28",
]
[project.urls]
Homepage = "https://github.com/IsuiGit/gigachat-controller"
Repository = "https://github.com/IsuiGit/gigachat-controller.git"

[tool.setuptools.packages.find]
where = ["src"]
