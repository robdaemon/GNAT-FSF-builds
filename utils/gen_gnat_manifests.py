#!/usr/bin/env python3

import wget
import subprocess
import sys
import tempfile
import os
import shutil

PKG_VERSION = "13.2.0-1"
CRATE_VERSION = "13.2.1"

targets = {
    "x86_64": {"crate": "gnat_native", "description": "Native"},
    "arm-elf": {"crate": "gnat_arm_elf", "description": "ARM cross-compiler"},
    "aarch64-elf": {"crate": "gnat_aarch64_elf", "description": "AArch64 cross-compiler"},
    "avr-elf": {"crate": "gnat_avr_elf", "description": "RISC-V cross-compiler"},
    "riscv64-elf": {"crate": "gnat_riscv64_elf", "description": "AVR cross-compiler"},
}


def check_sha256(package):
    base_url = f"https://github.com/alire-project/GNAT-FSF-builds/releases/download/gnat-{PKG_VERSION}/"
    pkg_url = base_url + package
    sha_file = package + ".sha256"
    sha_url = base_url + sha_file

    parent_dir = os.getcwd()
    temp_dir = tempfile.mkdtemp()
    try:
        os.chdir(temp_dir)
        print(f"Downloading {pkg_url}")
        wget.download(pkg_url)
        print()
        print(f"Downloading {sha_url}")
        wget.download(sha_url)
        print()

        sha256_hash = (
            subprocess.check_output(["sha256sum", package])
            .decode("utf-8")
            .split(" ")[0]
        )

        with open(sha_file, "r", encoding="utf-8") as file:
            sha256_hash_from_release = file.read()

        if sha256_hash != sha256_hash_from_release:
            print(f"invalid sha256 for {package}:")
            print(f" From GitHub release: {sha256_hash_from_release}")
            print(f" Actual             : {sha256_hash}")
            sys.exit(1)
    finally:
        os.chdir(parent_dir)
        shutil.rmtree(temp_dir)

    return sha256_hash


for target, params in targets.items():
    CRATE = params["crate"]
    TARGET_DESC = params["description"]

    linux_host = "linux" if target == "x86_64" else "linux64"
    linux_package = f"gnat-{target}-{linux_host}-{PKG_VERSION}.tar.gz"
    windows_package = f"gnat-{target}-windows64-{PKG_VERSION}.tar.gz"
    macos_package = f"gnat-{target}-darwin-{PKG_VERSION}.tar.gz"

    linux_sha256 = check_sha256(linux_package)
    windows_sha256 = check_sha256(windows_package)
    macos_sha256 = check_sha256(macos_package)

    MANIFEST_CONTENT = f"""
name = "{CRATE}"
version = "{CRATE_VERSION}"
provides = ["gnat={CRATE_VERSION}"]
description = "The GNAT Ada compiler - {TARGET_DESC}"
maintainers = ["chouteau@adacore.com"]
maintainers-logins = ["Fabien-Chouteau"]
licenses = "GPL-3.0-or-later AND GPL-3.0-or-later WITH GCC-exception-3.1"

auto-gpr-with = false

[configuration]
disabled = true

[environment]
PATH.prepend = "${{CRATE_ROOT}}/bin"

[origin."case(os)".linux."case(host-arch)".x86-64]
url = "https://github.com/alire-project/GNAT-FSF-builds/releases/download/gnat-{PKG_VERSION}/{linux_package}"
hashes = ["sha256:{linux_sha256}"]

[origin."case(os)".windows."case(host-arch)".x86-64]
url = "https://github.com/alire-project/GNAT-FSF-builds/releases/download/gnat-{PKG_VERSION}/{windows_package}"
hashes = ["sha256:{windows_sha256}"]

[origin."case(os)".macos."case(host-arch)".x86-64]
url = "https://github.com/alire-project/GNAT-FSF-builds/releases/download/gnat-{PKG_VERSION}/{macos_package}"
hashes = ["sha256:{macos_sha256}"]
"""

    MANIFEST_DIR = os.path.join("index", CRATE[0:2], CRATE)
    MANIFEST_FILE = os.path.join(MANIFEST_DIR, f"{CRATE}-{CRATE_VERSION}.toml")
    os.makedirs(MANIFEST_DIR, exist_ok=True)
    with open(MANIFEST_FILE, "w", encoding="utf-8") as file:
        file.write(MANIFEST_CONTENT)
