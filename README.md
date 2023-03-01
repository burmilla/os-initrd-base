# Initrd-base for BurmillaOS
This repository is used to build initrd base for BurmillaOS.

## How to contribute
- Fork this repository and create new branch based on master branch.
- Check what is latest [buildroot LTS version](https://buildroot.org/download.html) and update BUILDROOT_VERSION value Dockerfile.dapper
- Re-configure (needed to handle updated/changed packages):
```bash
make config
```
- Save changes
- Copy new configs over to old ones which is stored to GIT:
```bash
cp dist/artifacts/busybox-dynamic.config config/busybox-dynamic.config
cp dist/artifacts/buildroot-config-static config/amd64/buildroot-config-static
```
- Test build with command:
```bash
ARCH=amd64 RELEASE_VERSION=yyyy.mm.dd-test make release
```

## Contact
For bugs, questions, comments, corrections, suggestions, etc., open an issue in
 [burmilla/os](//github.com/burmilla/os/issues) with a title starting with `[os-initrd-base] `.

Or just [click here](//github.com/burmilla/os/issues/new?title=%5Bos-initrd-base%5D%20) to create a new issue.


## License
Copyright (c) 2020-2023 BurmillaOS community

Copyright (c) 2014-2020 [Rancher Labs, Inc.](http://rancher.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
