# aarch64 better build guide

A program for an AArch64 machine that inspects the CPU IDs and Linux hardware capability bits and reports the GCC AArch64 CPU/GCC definitions and feature relationships used by the supplied GCC / util-linux sources (upstream).

The project does **not** modify the upstream source files. The files under `upstream/` are inputs and can be replaced wholesale when moving to another upstream source revision.

## Upstream source inputs

The project uses these seven AArch64 GCC input paths:

https://github.com/gcc-mirror/gcc

- `gcc/common/config/aarch64/cpuinfo.h`
- `gcc/config/aarch64/aarch64-arches.def`
- `gcc/config/aarch64/aarch64-cores.def`
- `gcc/config/aarch64/aarch64-feature-deps.h`
- `gcc/config/aarch64/aarch64-option-extensions.def`
- `gcc/config/aarch64/aarch64.cc`
- `gcc/libgcc/config/aarch64/cpuinfo.c`

The util-linux ARM CPU-name database is also tracked as a source input:

https://github.com/util-linux/util-linux

- `util-linux/sys-utils/lscpu-arm.c`

The fallback lookup follows the supplied `lscpu-arm.c` data structure directly: first compare the CPU `implementer` with the first field of `hw_implementer[]`; use the matching entry's `parts` pointer, then compare the CPU `part` with the first field of the corresponding `id_part[]` entry and use its second field as the product name.

`aarch64-option-extensions.def` is used as the authoritative source for `AARCH64_FMV_FEATURE`, `IDENT`, `REQUIRES`, and `FEATURE_STRING`. The generator reconstructs the transitive `REQUIRES` closure in the same direction as `aarch64-feature-deps.h`'s `get_enable()`.

`aarch64-feature-deps.h` itself is tracked as an input. The standalone generator reconstructs the relevant `get_enable()` closure from the `REQUIRES` definitions in `aarch64-option-extensions.def`; it does not attempt to compile or copy the C++ implementation from this header. See `SOURCE_STATUS.md` for the status of the two newly added source inputs.

## Target Platform

aarch64 better build guide works on these platforms.

- Linux aarch64 (checked on Ubuntu 24.04 / 26.04) / glibc - please use for linux from releases.
- Android with Termux / bionic - please use for android from releases.
- Android with Linux Terminal (Debian) / glibc - please use for linux from releases.

## How to Use

Download binary file on releases and execute file as program. In android (termux),

```
chmod +x aarch64-better-build-guide-v0.0.1-android-aarch64
./aarch64-better-build-guide-v0.0.1-android-aarch64
```

Output:

```
  implementer=0x41 part=0xd80 variant=0x0 : 2 core(s)
  implementer=0x41 part=0xd81 variant=0x0 : 5 core(s)
  implementer=0x41 part=0xd82 variant=0x0 : 1 core(s)
CPU matched GCC options with runtime derived modifiers:
  implementer=0x41 part=0xd80 variant=0x0
    -mcpu=cortex-a520+nosve+nossbs+nowfxt+nomemtag
    -march=armv9.2-a+nosve+nossbs+nowfxt+nomemtag
    -mtune=cortex-a520
  implementer=0x41 part=0xd81 variant=0x0
    -mcpu=cortex-a720+nosve+nossbs+nowfxt+nomemtag
    -march=armv9.2-a+nosve+nossbs+nowfxt+nomemtag
    -mtune=cortex-a720
  implementer=0x41 part=0xd82 variant=0x0
    -mcpu=cortex-x4+nosve+nossbs+nowfxt+nomemtag
    -march=armv9.2-a+nosve+nossbs+nowfxt+nomemtag
    -mtune=cortex-x4

For more detailed information, add -v/--verbose.
```

Your CPU information and inferred GCC compile flags(`-mcpu` / `-march` / `-mtune`) will display.

When device's CPU doesn't defined in GCC sources, result will change with util-linux definition. In these case, only `-march` will display because CPU core doesn't defined in GCC source and `-march` value will be `armv8-a+features`.

Qualcomm Snapdragon 665 (dtab d-41A docomo) :

```
  implementer=0x51 part=0x801 variant=0xa : 4 core(s)
  implementer=0x51 part=0x800 variant=0xa : 4 core(s)
CPU matched GCC options with runtime derived modifiers:
  implementer=0x51 part=0x801 variant=0xa -> -march=armv8-a+crc+sha2+aes
  implementer=0x51 part=0x800 variant=0xa -> -march=armv8-a+crc+sha2+aes
  
For more detailed information, add -v/--verbose.
```

Qualcomm Snapdragon 845 (SONY Xperia XZ3) :

```
  implementer=0x51 part=0x803 variant=0x7 : 4 core(s)
  implementer=0x51 part=0x802 variant=0x6 : 4 core(s)
CPU matched GCC options with runtime derived modifiers:
  implementer=0x51 part=0x803 variant=0x7 -> -march=armv8-a+lse+crc+sha2+aes+fp16
  implementer=0x51 part=0x802 variant=0x6 -> -march=armv8-a+lse+crc+sha2+aes+fp16
  
For more detailed information, add -v/--verbose.
```

[Various results are in Examples.md](EXAMPLE.md)

## What is reported

For each detected CPU ID, the program preserves the Linux-style ID spelling and counts how many `/proc/cpuinfo` processor records carry that exact implementer/part/variant tuple. The count is reported as the number of logical CPUs represented by that ID, for example:

```text
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd05 variant=0x2 : 4 core(s)
  implementer=0x41 part=0xd0b variant=0x4 : 4 core(s)
```

`AARCH64_BIG_LITTLE(big, little)` is treated as a two-part CPU record, so a system exposing both `0xd0b` and `0xd05` from implementer `0x41` matches the supplied `cortex-a76.cortex-a55` record.

The report then shows:

1. Runtime `FEAT_*` bits detected by the supplied `cpuinfo.c`.
2. Runtime `FEAT_*` bits not detected.
3. For every non-hidden `FEAT_*`, its direct GCC FMV `OPT_FLAGS`, the transitive GCC `REQUIRES` closure, and its Linux `/proc/cpuinfo` `FEATURE_STRING` condition when one is defined.
4. Every distinct `FLAGS` used by `aarch64-cores.def`, and whether the supplied `aarch64-option-extensions.def` gives it a direct `FEAT_*` FMV mapping.

Examples of the intended output form:

```text
FEAT_* -> GCC FLAGS / GCC dependency closure / Linux runtime condition:
  FEAT_DOTPROD (DOTPROD)
    GCC requires: DOTPROD and SIMD and FP
    runtime condition: asimddp

  FEAT_FP16 (F16)
    GCC requires: F16 and FP
    runtime condition: fphp asimdhp

  FEAT_SVE_PMULL128 (SVE2 AND SVE_AES)
    GCC requires: SVE2 and SVE_AES and SVE and SIMD and FP and AES ...
    runtime condition: sveaes | smeaes
```

The displayed `GCC requires` line is the transitive GCC dependency closure, while `runtime condition` is the Linux feature-string condition from `aarch64-option-extensions.def`. They are deliberately kept separate.

Some `aarch64-cores.def` flags have no direct `FEAT_*` FMV mapping in the supplied sources. For those, the program says so instead of inventing a mapping. This is important for flags such as `PROFILE`, `PAUTH`, `LS64`, and the `CRYPTO` alias: absence of a `FEAT_*` entry is source information, not an inferred equivalence.

### GCC `-mcpu`, `-march`, and `-mtune` output

When a CPU ID matches a GCC definition, the report emits three GCC option forms:

- `-mcpu=<core>[+feature...]`: the GCC product/core name plus runtime-supported core-specific modifiers and any required `+no...` corrections.
- `-march=<architecture>[+feature...]`: the GCC architecture spelling corresponding to the `V8A`/`V8_2A`/`V9_2A`-style architecture identifier in `aarch64-cores.def`, plus the applicable modifiers.
- `-mtune=<core>`: only the core name. GCC explicitly does not allow feature modifiers on `-mtune` (`This option cannot be suffixed by feature modifiers.`), so the program never appends `+...` to `-mtune`.

Positive modifiers are emitted only when the supplied GCC sources provide a runtime `FEAT_*` representation for the corresponding core flag and that runtime feature is present. Extensions already included by the selected architecture baseline are omitted rather than repeated. The report then prints the complete architecture-baseline modifier reference for that `-march`/`-mcpu` result, including examples such as:

```text
fp   (omitted by including in armv8-a)
crc  (omitted by including in armv8.1-a)
lse  (omitted by including in armv8.1-a)
rdma (omitted by including in armv8.1-a)
pauth (omitted by including in armv8.3-a)
```

The reference list distinguishes an architecture omission from a runtime mismatch. If an architecture-baseline feature is normally provided by the selected architecture but is absent from the runtime CPU feature mask, the final option string receives a `+no...` modifier instead. Dependency parents are preferred so redundant child options are suppressed; for example, a missing SVE prerequisite is represented by `+nosve` rather than separately spelling every dependent SVE2 extension. Flags without a runtime representation are not guessed.

The architecture name and architecture baseline are generated from GCC's `aarch64-arches.def`. The generator recursively expands the `AARCH64_ARCH(..., FLAGS)` inheritance and then resolves each extension through the `REQUIRES` data in `aarch64-option-extensions.def`, matching the `get_enable()` direction used by `aarch64-feature-deps.h`. This is what makes entries such as `FRINTTS` appear under `armv8.5-a` and, through the architecture inheritance chain, under `armv9.2-a`.

For each baseline option the generator also records the first architecture in the supplied `aarch64-arches.def` sequence that introduced it. The omission reference therefore uses the actual introduction point, for example:

```text
frintts (omitted by including in armv8.5-a)
```

The architecture baseline is no longer maintained as a hand-written table in `src/main.cpp`. When moving to another GCC revision, replace `aarch64-arches.def` together with the other GCC inputs and rebuild; the architecture inheritance table is regenerated automatically.

### Runtime-constrained `-mcpu` option

When a CPU ID matches a GCC definition, the program also compares the core's transitive feature closure with the `FEAT_*` bits actually detected by the supplied upstream `cpuinfo.c`. For runtime-detectable features that are required by that matched core but are absent at runtime, it emits GCC `+no...` modifiers. Dependency parents are preferred so redundant child disables are omitted.

For example, the supplied GCC record for `cortex-x4` is:

```text
FLAGS: SVE2_BITPERM, MEMTAG, PROFILE
```

If the runtime mask has `FEAT_SVE` and `FEAT_MEMTAG2` clear, while the other prerequisites are present, the report can produce:

```text
CPU-matched GCC core options with runtime-derived modifiers:
  0x41/0xd82 -> -mcpu=cortex-x4+nosve+nomemtag
```

This is deliberately conditional on the CPU ID matching the GCC definition. The program does not add `+no...` to an unmatched CPU. It also does not invent negative options for core flags that have no corresponding runtime `FEAT_*` FMV feature in the supplied sources (for example `PROFILE`).

The `+no...` list is a runtime compatibility constraint, not a claim about GCC's complete internal `-mcpu=native` selection algorithm. It is intended to express the important case where the GCC definition contains an ISA extension that the running kernel/GCC `cpuinfo.c` feature mask does not report.

## Replacing GCC sources

Replace the seven GCC files under `upstream/gcc/` and the util-linux `lscpu-arm.c` source under `upstream/util-linux/sys-utils/` with the corresponding files from the new GCC source tree, preserving the paths. Then rebuild from a clean build directory if desired:

```sh
rm -rf build
cmake -S . -B build -G Ninja
cmake --build build
```

No edits to those GCC files are required.

### MEMTAG / Arm FEAT_MTE

The Arm architectural feature is commonly referred to as FEAT_MTE (Memory Tagging Extension), while the GCC AArch64 option-extension spelling in the supplied GCC sources is `memtag`. Therefore the generated GCC modifiers are `+memtag` and `+nomemtag`; the detector maps the runtime `FEAT_MEMTAG2` representation to GCC's `MEMTAG` flag.

## GCC-unmatched CPU fallback

The fallback is used **only when no GCC AArch64 definition matches the observed CPU IDs**. It does not run for a CPU that GCC has already identified.

On the unmatched path, the program checks the runtime `FEAT_FP` and `FEAT_SIMD` bits from the supplied GCC `cpuinfo.c`. Only when **both** are present does it select:

```text
-march=armv8-a[+CPU-flags...]
```

The CPU flags are taken from runtime-detected `FEAT_*` entries that have a direct GCC option mapping in `aarch64-option-extensions.def`. Options already provided by the `armv8-a` baseline are not repeated. No CPU-specific `-mcpu` or `-mtune` is invented for an unmatched GCC CPU.

The fallback `-march` is emitted **for every observed logical-CPU type**. If `/proc/cpuinfo` contains multiple implementer/part/variant combinations, each combination receives its own `-march` line. The runtime feature mask supplied by the upstream GCC `cpuinfo.c` is process-wide, so when the available runtime evidence is identical the resulting modifier suffix can also be identical across those lines.

The util-linux database is used for the CPU vendor/product identification shown in verbose fallback output. The lookup follows `hw_implementer[]` first, then the selected `id_part[]` array, and uses the matched `id_part` name as the product name.

If either `FEAT_FP` or `FEAT_SIMD` is absent, the fallback `-march=armv8-a` is not emitted.

## Important scope

This tool reports the CPU/core and feature relationships represented by the supplied GCC sources. It is not a reimplementation of the entire GCC `-mcpu=native` option parser or scheduler/tuning selection. In particular, a core's `FLAGS`, architecture, scheduler, and tuning parameters are distinct GCC concepts. The report therefore does not claim that a single runtime HWCAP mask by itself reproduces every internal decision made by GCC's full `-mcpu=native` option machinery. Omitted-feature reasons are informational and distinguish architecture inclusion from the absence of a runtime `FEAT_*` mapping.

## Testing with a saved `/proc/cpuinfo`

For parser/runtime regression testing without modifying the program's production default, set `AARCH64_NATIVE_MCPU_CPUINFO` to a file containing Linux-style CPU ID records. If unset, `/proc/cpuinfo` is used.

For example:

```text
processor : 0
CPU implementer : 0x41
CPU part : 0xd80
CPU variant : 0x0

processor : 1
CPU implementer : 0x41
CPU part : 0xd81
CPU variant : 0x0

processor : 2
CPU implementer : 0x41
CPU part : 0xd82
CPU variant : 0x0
```

On a real AArch64 system the runtime feature mask still comes from the supplied upstream `cpuinfo.c`; the environment variable only changes where the CPU ID records are read from.

## v8 architecture-baseline omission reference

The normal report is assembled into `std::ostringstream` sections before the
final report is written. The program does not stream individual report lines
directly to `std::cout`; the normal report is emitted as one completed string.
The JSON mode follows the same pattern and emits one completed JSON document.

For each matched GCC core, the option section includes a reference list of
architecture-baseline and core-specific feature modifiers that were not
written as `+feature`. Each item includes the reason. For example:

```text
omitted feature modifiers (reference; architecture baseline and core-specific omissions):
  fp (omitted by including in armv8-a)
  crc (omitted by including in armv8.1-a)
  lse (omitted by including in armv8.1-a)
  rdma (omitted by including in armv8.1-a)
  pauth (omitted by including in armv8.3-a)
```

If an architecture-baseline feature is normally provided by the selected
architecture but is absent from the runtime CPU feature mask, the final
option string receives a `+no...` modifier. Dependency parents are preferred.
For example, for `armv9.2-a`, if SVE is absent, the report can say:

```text
sve2 (omitted by including in armv9.2-a; runtime feature is unavailable, so +nosve is emitted)
```

Features with no runtime `FEAT_*` representation are not guessed. Their
architecture inclusion is still reported when the selected architecture
baseline contains the corresponding GCC option.

CPU ID counts use the requested `core(s)` spelling, for example:

```text
implementer=0x41 part=0xd05 variant=0x2 : 4 core(s)
```

## Command-line output

With no arguments, the program prints only the CPU implementer/part/variant and logical-CPU count, followed by the `-mcpu`, `-march`, and `-mtune` portions of the GCC option result. For an unmatched GCC definition, the per-CPU-type fallback `-march` lines are shown. The output ends with:

```text
For more detailed information, add -v/--verbose.
```

`-v` and `--verbose` print the previous detailed report, including runtime features, FEAT/GCC mappings, GCC definitions, fallback details, and the upstream source attribution.

In the `FEAT_* -> GCC FLAGS / GCC dependency closure / Linux runtime condition` section, only the displayed `GCC requires` connectors use lowercase `and`/`or`. The Linux runtime condition preserves the uppercase `AND`/`OR` spelling derived from the source expression.

## Build

### prerequisite

- CMake
- Ninja (ninja-build in Ubuntu)
- Python3
- gcc / g++ or clang

```sh
cmake -S . -B build -G Ninja
cmake --build build
```

Run:

```sh
./build/aarch64-better-build-guide
```

JSON output is available with:

```sh
./build/aarch64-better-build-guide --json
```

The program is intended to be built and run natively on AArch64. In particular, the `cpuinfo.c` object is compiled as part of this executable so that the runtime CPU feature mask follows the supplied GCC `cpuinfo.c` logic rather than a hand-written HWCAP parser.
