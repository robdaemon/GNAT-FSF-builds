# GNAT-FSF-builds
Builds of the GNAT Ada compiler from FSF GCC releases

# Notes on this fork

This fork adds the aarch64-elf target with a rpi3 runtime.

## How to build this fork

To start the builds you will need `python3` and the `e3-core` package.
This can be done in a virtual env, e.g.:

```console
$ python3 -m venv my-virtual-env
$ source my-virtual-env/bin/activate
$ pip install e3-core==22.1.0
```

It is suggested you build gprbuild / gprconfig via this repository also, on Ubuntu 24.04 the `gprbuild` package is an
older version that will not properly recognize the toolchain.

```console
$ ./anod build release_package --qualifier=package=gprbuild --target=aarch64-elf  -v --loglevel DEBUG
```

This will generate the tarball at `./sbx/x86_64-linux/release_package-gprbuild-x86_64-linux/install/gprbuild-x86_64-linux-24.0.0-1.tar.gz`
that includes `gprbuild` and `gprconfig` and other tools. 

Now, to build the cross-compiler:

```console
$ ./anod build release_package --qualifier=package=gnat --target=aarch64-elf  -v --loglevel DEBUG
```

This will generate a tarball at `./sbx/aarch64-elf-linux64/release_package-gnat-aarch64-elf-linux64/install` that
includes the compiler, gdb, and the `embedded-rpi3`, `light-rpi3` and `light-tasking-rpi3` RTSes, but does not include
`gprbuild` or other components.

## Installing the AArch64 toolchain

You'll want to extract this tarball from the previous section somewhere, something like `$HOME/arm`, and then add it
to your `PATH`, like the following:

```console
$ mkdir $HOME/arm
$ cd $HOME/arm
$ tar xf $HOME/src/GNAT-FSF-builds/sbx/aarch64-elf-linux64/release_package-gnat-aarch64-elf-linux64/install/gnat-aarch64-elf-linux64-14.1.0-2.tar.gz
```

# How to build

To start the builds you will need `python3` and the `e3-core` package.
This can be done in a virtual env, e.g.:
```console
$ python3 -m venv my-virtual-env
$ source my-virtual-env/bin/activate
$ pip install e3-core==22.1.0
```

To build a spec, for example `mpc`, run the `anod` script:
```console
$ ./anod build mpc -v --loglevel DEBUG
```

`-v --loglevel DEBUG` will produce many information log about the build.

For a cross compiler:

```console
$ ./anod build gcc --target=avr-elf -v --loglevel DEBUG
```


## On Windows
Only builds in the msys2 mingw64 environement are supported.
You will need:

 - `mingw-w64-x86_64-python-psutil` package for `e3-core` installation to work.

 - The Unix and Windows PATH of the repo checkout must match:
   `C:\dir1\dir2\GNAT-FSF-builds` <-> `\dir1\dir2\GNAT-FSF-builds`. This can be
   done by "mounting" Windows directories in msys2, e.g.: `mount C:/Users
   /Users`.

# Writing specs
Until the `e3-core`/`anod` documentation is available online, the best way to
write a spec is to start from an existing one. A good starting point would be
[`gnatcoll.anod`](https://github.com/alire-project/GNAT-FSF-builds/blob/main/specs/gnatcoll.anod).

 - First, change the `version`, `tarball` and, `source_pkg_build` url
 - Modify the list of `build_deps`, you probably need at least `gcc`.
 - Change the configure/make options

# Publishing to the Alire index

A [little script](utils/gen_gnat_manifests.py) is available to speedup the
process of publising GNAT FSF package to the Alire index.

Edit the PKG_VERSION and CRATE_VERSION constant and then run the script to
generate all the GNAT manifests. The script also checks the correctness of
sha256 hashes.
