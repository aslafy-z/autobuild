# Autobuild

Automatically build a Docker image from a GitHub repository upon a pull request.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Overview

The `autobuild` repository provides a simple mechanism to automatically build a Docker image whenever a pull request is made to the repository. This is particularly useful for continuous integration and deployment workflows, ensuring that the latest changes are always reflected in the Docker image.

## Features

- **Automatic Docker Image Builds**: Trigger Docker image builds on pull requests.
- **GitHub Integration**: Seamlessly integrates with GitHub repositories.
- **Customizable**: Easily modify the build process to suit your needs.

## Requirements

- Docker
- Python 3.7+
- GitHub repository with pull request events

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aslafy-z/autobuild.git
   cd autobuild
  
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure your GitHub repository to trigger the build process on pull request events.
2. Ensure that the repository contains a valid `Dockerfile` and any necessary build context.
3. The system will automatically build the Docker image upon receiving a pull request.

## File Structure

```
autobuild/
├── .gitignore             # Git ignore file
├── Dockerfile             # Dockerfile for building the image
├── LICENSE                # Project license
├── README.md              # Project documentation
├── app.py                 # Main application script
├── renovate.json          # Renovate configuration
└── requirements.txt       # Python dependencies
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
