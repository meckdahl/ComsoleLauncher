# Pre-built Wheels

This folder contains pre-built Python wheels for Windows to avoid requiring Visual C++ Build Tools.

## Included

**JPype1 1.6.0** - Python 3.13 (Windows 64-bit)
- License: Apache License 2.0
- Source: https://github.com/jpype-project/jpype
- PyPI: https://pypi.org/project/JPype1/

## Apache License 2.0 (JPype1)

```
Copyright 2004-2024 JPype Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Building for Other Python Versions

To add wheels for different Python versions:

```bash
# Install target Python version first
pip download jpype1 --only-binary :all: --platform win_amd64 --python-version 3.X --dest wheels/ --no-deps
```
