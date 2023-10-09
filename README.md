# Regular Expression Engine Course Project

Welcome to the Regular Expression Engine course project repository! This repository contains a simple implementation of a Regular Expression Engine in Go. We aim to imitate the `egrep`. This project was created as part of a DAAR course at Sorbonne University to help you understand the inner workings of regex engines.

## Table of Contents
- [Regular Expression Engine Course Project](#regular-expression-engine-course-project)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Cloning and Building](#cloning-and-building)
  - [Contributing](#contributing)

## Introduction

Regular expressions are a powerful tool for text pattern matching and manipulation. This project aims to demystify how regular expression engines work under the hood by providing a simple implementation. By exploring this codebase, you'll gain a deeper understanding of how regex engines parse and match text.

## Features

Our Regular Expression Engine offers the following features:

- **Basic Matching**: It can match simple regular expressions with characters like letters, digits, and special characters.
- **Quantifiers**: Basic quantifiers like `*`, and `+` are supported.


## Getting Started

### Prerequisites
Before testing the project it is required to have the following technologies installed.
- [PyInstaller](https://pyinstaller.org/en/stable/) refer to the installation guide to install.
- [Makefile](https://tldp.org/HOWTO/Software-Building-HOWTO-3.html): refer to the installation guide to install.
- [Git](https://git-scm.com/downloads): refer to the installation guide to install.

### Cloning and Building

To get started with this Regular Expression Engine, follow these steps:

1. Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/ubombar/daar-regex-engine.git
   ```

2. Change the directory to the project folder:

   ```bash
   cd daar-regex-engine
   ```

3. Run the following command to build the executable. Note that to before building it is reccomended to *clean* the project. Additionally, building the project requires you to install `pyinstaller`. You can find 

   ```bash
   make clean
   make build
   ```

4. (Optional) If you want to do a performance test you can use the `make test` command.

## Contributing

We welcome contributions from the community to improve this Regular Expression Engine project. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your contributions and commit them with clear messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

Please ensure your code adheres to good coding practices and includes appropriate documentation.
