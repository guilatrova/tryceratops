# Changelog

<!--next-version-placeholder-->

## v1.2.0 (2023-04-29)
### Feature
* Handle false positive for TC300 ([`719d07f`](https://github.com/guilatrova/tryceratops/commit/719d07f46dc68d4036964216c65aafdf452366da))

### Documentation
* Fix syntax err in TC003 ([`130a7f2`](https://github.com/guilatrova/tryceratops/commit/130a7f2a512aaeefb6bb7faaced75d8865ce9b26))
* Add poetry install option ([`fa50c28`](https://github.com/guilatrova/tryceratops/commit/fa50c2840b2ff3afc2c57d136d921b1dba54fc57))
* Update readme ([`9291efb`](https://github.com/guilatrova/tryceratops/commit/9291efb9a159cbfbd9db6127944bac2fd6aa3dd2))

## v1.1.0 (2022-04-30)
### Feature
* Reduce dependencies contraints ([`1a71007`](https://github.com/guilatrova/tryceratops/commit/1a710072c86f4747a375e0bcd88766e856baeaf9))

### Documentation
* Update contributing with gitmessage ([`0bd7c61`](https://github.com/guilatrova/tryceratops/commit/0bd7c61e4004919483ae86611a1a1a5ea1555486))
* Replace logo ([`38bd6cd`](https://github.com/guilatrova/tryceratops/commit/38bd6cdb95e57bd9674fd5b061abef63ec94c85e))

## v1.0.1 (2021-12-31)
### Fix
* Open files with utf-8 encoding for windows ([`a46636c`](https://github.com/guilatrova/tryceratops/commit/a46636ccce68742cf83f035507c4680357cabb14))

### Documentation
* Update badges ([`2308e9d`](https://github.com/guilatrova/tryceratops/commit/2308e9ddbbc320b0ad43a7e959cba2d6eaa14526))

## v1.0.0 (2021-11-22)
### Feature
* Add prefer `TypeError` analyzer ([`ac75e37`](https://github.com/guilatrova/tryceratops/commit/ac75e377b8c6213f549fccc45a4d34db2c73404c))

### Breaking
* add prefer `TypeError` analyzer ([`ac75e37`](https://github.com/guilatrova/tryceratops/commit/ac75e377b8c6213f549fccc45a4d34db2c73404c))

### Documentation
* Add `TypeError` violation ([`d424e7c`](https://github.com/guilatrova/tryceratops/commit/d424e7c0bd4ce8364ad6dd8f47c08619e5bbd6de))
* Make tryceratops use case more obvious ([`36f1292`](https://github.com/guilatrova/tryceratops/commit/36f1292e3e4bbd6a2bb1201069d1a902e8b68360))
* Update badges ([`eb3c162`](https://github.com/guilatrova/tryceratops/commit/eb3c1624c9a79e4341151ecc884d338f51217ac2))

## v0.6.1 (2021-11-17)
### Fix
* **windows:** Remove emojis from presentation ([`e7f6bbe`](https://github.com/guilatrova/tryceratops/commit/e7f6bbec1dfb525aacd1a30c8e737b27ef93efd9))

### Documentation
* Add extra resource ([`259bf9c`](https://github.com/guilatrova/tryceratops/commit/259bf9c1eb357f2ebf737f5b3f9c52220645490f))

## v0.6.0 (2021-09-12)
### Feature
* Add cheerful message when no violations ([`bff695c`](https://github.com/guilatrova/tryceratops/commit/bff695c90bf08d9e5489376407f64e1af71d26ad))
* Block autofix when using flake8 ([`77d6af3`](https://github.com/guilatrova/tryceratops/commit/77d6af33b60bef51f7f0a5ed80ee6f0965d57856))
* **fixers:** Implement fixer for logging error ([`f488cee`](https://github.com/guilatrova/tryceratops/commit/f488cee1181610d40f65bc328a802c2a772a951c))
* **fixers:** Capture exceptions ([`ee708a4`](https://github.com/guilatrova/tryceratops/commit/ee708a42ca1b154a00a9ccae26c87d0243f184c5))
* **fixers:** Run all fixers when enabled ([`3db7e05`](https://github.com/guilatrova/tryceratops/commit/3db7e056981fcf8a4a7926bf97245540728f56f0))
* **fixers:** Handle multiline reraise ([`c1f14b0`](https://github.com/guilatrova/tryceratops/commit/c1f14b03d28bef2626d451cbffd3c93faee19461))
* **fixers:** Implement fixer for reraise no cause ([`2f9d46d`](https://github.com/guilatrova/tryceratops/commit/2f9d46d864b35f8ad4af6b8aac240c6dcb79a775))
* Include fixers to run ([`e885b34`](https://github.com/guilatrova/tryceratops/commit/e885b34ca0d2354735f5d89f0a6f488ace24cb2c))
* **fixers:** Add fixer for reraise ([`041f67f`](https://github.com/guilatrova/tryceratops/commit/041f67ffc1df900b3d0e1ea37c27f73ab7f45097))
* Add --autofix flag ([`1428958`](https://github.com/guilatrova/tryceratops/commit/142895827a3da801a470efb54a2d4e4b9687952a))

### Fix
* Use Dict to support Python 3.8 ([`22e4119`](https://github.com/guilatrova/tryceratops/commit/22e4119802db8a205929bf70c2c2657cb36a290d))
* **fixers:** Count fixed violations correctly ([`825794c`](https://github.com/guilatrova/tryceratops/commit/825794c76cb6c7b712e52e8ec4989d7edf98f8ee))
* **fixers:** Reset offset between writes ([`dc3a070`](https://github.com/guilatrova/tryceratops/commit/dc3a070f1a51eadaaec3fbf623d0d99a71b964e0))
* Trim only exception name ([`18af429`](https://github.com/guilatrova/tryceratops/commit/18af429a89537f543652cb4fddf757d9073c68d9))

### Documentation
* Update sample image ([`dd4ff40`](https://github.com/guilatrova/tryceratops/commit/dd4ff40f47c17412b46bafcbc96131c37b0f2c99))
* Add autofix instructions ([`3c64f36`](https://github.com/guilatrova/tryceratops/commit/3c64f36d29ebe18dc568b5c985b73512f5d46e2a))

## v0.5.0 (2021-07-31)
### Feature
* **analyzers:** Add analyzer log exception object ([`b7385da`](https://github.com/guilatrova/tryceratops/commit/b7385da16ff68fa5320a86adf02ebd03efeb1c22))
* **analyzers:** Add analyzer for log error ([`4c755e5`](https://github.com/guilatrova/tryceratops/commit/4c755e54d7f324eb3e5937cd501bb09e9493fae3))

### Documentation
* Add sample for TC401 (logging w/o object) ([`875ce09`](https://github.com/guilatrova/tryceratops/commit/875ce09f5efbaccdd555ffe4bd3cdb4ab6c38b4b))
* Add sample for TC400 (logging.exception) ([`a74d97b`](https://github.com/guilatrova/tryceratops/commit/a74d97be73bb1e12e50d2bb3721a0169c0a40ade))

## v0.4.0 (2021-07-30)
### Feature
* Add verbose flag ([`95a34b6`](https://github.com/guilatrova/tryceratops/commit/95a34b643ad71c392d419006607ba4d3cbb68375))

## v0.3.0 (2021-07-21)
### Feature
* Rename 'notc' tokens to become 'noqa' ([`0a2c1c5`](https://github.com/guilatrova/tryceratops/commit/0a2c1c5a9efe77c94a0080369ce2e18ae3e937b7))

### Breaking
* Any previous 'notc' token will stop working. Now you must use 'noqa' instead, which keeps consistent with flake8 standards  ([`0a2c1c5`](https://github.com/guilatrova/tryceratops/commit/0a2c1c5a9efe77c94a0080369ce2e18ae3e937b7))

### Documentation
* Add changelog to pypi and readme ([`9dac24b`](https://github.com/guilatrova/tryceratops/commit/9dac24b50b92e39abac63307345343189ccb24bf))

## v0.2.6 (2021-07-21)
### Fix
* **cli:** Return exit code for unprocessed ([`50df1dc`](https://github.com/guilatrova/tryceratops/commit/50df1dcb3f671062a76b280c994672a2313b9d38))

### Documentation
* Remove trailing whitespaces ([`983f8bf`](https://github.com/guilatrova/tryceratops/commit/983f8bf6aa8f96284a9a0e5f991a000a78b0753d))
* Add badges to README ([`8b7a140`](https://github.com/guilatrova/tryceratops/commit/8b7a140a45dbfee832e1b89a90c59d6a4abd3c44))
* Update CONTRIBUTING with automation ([`e2b40f6`](https://github.com/guilatrova/tryceratops/commit/e2b40f6099a22c879d85548bafc15bc89468824d))
* Add contributing ([`70bfa7d`](https://github.com/guilatrova/tryceratops/commit/70bfa7d403a833e3e575931938f4fd24028def52))
* Add extra resources section ([`07821cb`](https://github.com/guilatrova/tryceratops/commit/07821cb70a23de9e602929cab42d62aeef214383))
* Add the badge to the project ([`d31ac07`](https://github.com/guilatrova/tryceratops/commit/d31ac071e11370d20982538a0256ff4c984f5902))
* Add support badge ([`3b61817`](https://github.com/guilatrova/tryceratops/commit/3b618173cd8b5996a74e3ffc6c9833e53e504172))
* Add open on vscode badge ([`381877d`](https://github.com/guilatrova/tryceratops/commit/381877d1b34ed8f63da611ad4b6f0774d1ad65c0))
