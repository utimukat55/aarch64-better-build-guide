Various devices outputs without common definition

## Orange Pi 5 (Ubuntu 24.04)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd05 variant=0x2 : 4 core(s)
  implementer=0x41 part=0xd0b variant=0x4 : 4 core(s)

Matched GCC definitions (per observed CPU ID):
  0x41/0xd05 -> -mcpu=cortex-a55
  0x41/0xd0b -> -mcpu=cortex-a76
  GCC definition: -mcpu=cortex-a55  arch=V8_2A
    FLAGS: F16, RCPC, DOTPROD
  GCC definition: -mcpu=cortex-a76  arch=V8_2A
    FLAGS: F16, RCPC, DOTPROD
  GCC definition: -mcpu=cortex-a76.cortex-a55  arch=V8_2A  [BIG.LITTLE]
    FLAGS: F16, RCPC, DOTPROD

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_DOTPROD
  + FEAT_RDM
  + FEAT_LSE
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC
  + FEAT_SHA2
  + FEAT_PMULL
  + FEAT_FP16
  + FEAT_DPB
  + FEAT_RCPC

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_FLAGM
  - FEAT_FLAGM2
  - FEAT_FP16FML
  - FEAT_SM4
  - FEAT_CSSC
  - FEAT_SHA3
  - FEAT_DIT
  - FEAT_DPB2
  - FEAT_JSCVT
  - FEAT_FCMA
  - FEAT_RCPC2
  - FEAT_FRINTTS
  - FEAT_I8MM
  - FEAT_BF16
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SB
  - FEAT_SSBS2
  - FEAT_BTI
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

CPU-matched GCC options with runtime-derived modifiers:
  implementer=0x41 part=0xd05 variant=0x2 -> -mcpu=cortex-a55+fp16+rcpc+dotprod
     -march=armv8.2-a+fp16+rcpc+dotprod
     -mtune=cortex-a55
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
  implementer=0x41 part=0xd0b variant=0x4 -> -mcpu=cortex-a76+fp16+rcpc+dotprod
     -march=armv8.2-a+fp16+rcpc+dotprod
     -mtune=cortex-a76
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
```

## Raspberry Pi 4B (Ubuntu 26.04)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd08 variant=0x0 : 4 core(s)

Matched GCC definitions (per observed CPU ID):
  0x41/0xd08 -> -mcpu=cortex-a72
  GCC definition: -mcpu=cortex-a72  arch=V8A
    FLAGS: CRC

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_FLAGM
  - FEAT_FLAGM2
  - FEAT_FP16FML
  - FEAT_DOTPROD
  - FEAT_SM4
  - FEAT_RDM
  - FEAT_LSE
  - FEAT_CSSC
  - FEAT_SHA2
  - FEAT_SHA3
  - FEAT_PMULL
  - FEAT_FP16
  - FEAT_DIT
  - FEAT_DPB
  - FEAT_DPB2
  - FEAT_JSCVT
  - FEAT_FCMA
  - FEAT_RCPC
  - FEAT_RCPC2
  - FEAT_FRINTTS
  - FEAT_I8MM
  - FEAT_BF16
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SB
  - FEAT_SSBS2
  - FEAT_BTI
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

CPU-matched GCC options with runtime-derived modifiers:
  implementer=0x41 part=0xd08 variant=0x0 -> -mcpu=cortex-a72+crc
     -march=armv8-a+crc
     -mtune=cortex-a72
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
```

## Rapsberry Pi 3B (Ubuntu 24.04)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd03 variant=0x0 : 4 core(s)

Matched GCC definitions (per observed CPU ID):
  0x41/0xd03 -> -mcpu=cortex-a53
  GCC definition: -mcpu=cortex-a53  arch=V8A
    FLAGS: CRC

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_FLAGM
  - FEAT_FLAGM2
  - FEAT_FP16FML
  - FEAT_DOTPROD
  - FEAT_SM4
  - FEAT_RDM
  - FEAT_LSE
  - FEAT_CSSC
  - FEAT_SHA2
  - FEAT_SHA3
  - FEAT_PMULL
  - FEAT_FP16
  - FEAT_DIT
  - FEAT_DPB
  - FEAT_DPB2
  - FEAT_JSCVT
  - FEAT_FCMA
  - FEAT_RCPC
  - FEAT_RCPC2
  - FEAT_FRINTTS
  - FEAT_I8MM
  - FEAT_BF16
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SB
  - FEAT_SSBS2
  - FEAT_BTI
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

CPU-matched GCC options with runtime-derived modifiers:
  implementer=0x41 part=0xd03 variant=0x0 -> -mcpu=cortex-a53+crc
     -march=armv8-a+crc
     -mtune=cortex-a53
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
```

## Google Pixel 6a / Google Tensor (Termux)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd05 variant=0x2 : 4 core(s)
  implementer=0x41 part=0xd0b variant=0x4 : 2 core(s)
  implementer=0x41 part=0xd44 variant=0x1 : 2 core(s)

Matched GCC definitions (per observed CPU ID):
  0x41/0xd05 -> -mcpu=cortex-a55
  0x41/0xd0b -> -mcpu=cortex-a76
  0x41/0xd44 -> -mcpu=cortex-x1
  GCC definition: -mcpu=cortex-a55  arch=V8_2A
    FLAGS: F16, RCPC, DOTPROD
  GCC definition: -mcpu=cortex-a76  arch=V8_2A
    FLAGS: F16, RCPC, DOTPROD
  GCC definition: -mcpu=cortex-x1  arch=V8_2A
    FLAGS: F16, RCPC, DOTPROD, SSBS, PROFILE
  GCC definition: -mcpu=cortex-a76.cortex-a55  arch=V8_2A  [BIG.LITTLE]
    FLAGS: F16, RCPC, DOTPROD

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_DOTPROD
  + FEAT_RDM
  + FEAT_LSE
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC
  + FEAT_SHA2
  + FEAT_PMULL
  + FEAT_FP16
  + FEAT_DPB
  + FEAT_RCPC

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_FLAGM
  - FEAT_FLAGM2
  - FEAT_FP16FML
  - FEAT_SM4
  - FEAT_CSSC
  - FEAT_SHA3
  - FEAT_DIT
  - FEAT_DPB2
  - FEAT_JSCVT
  - FEAT_FCMA
  - FEAT_RCPC2
  - FEAT_FRINTTS
  - FEAT_I8MM
  - FEAT_BF16
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SB
  - FEAT_SSBS2
  - FEAT_BTI
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

CPU-matched GCC options with runtime-derived modifiers:
  implementer=0x41 part=0xd05 variant=0x2 -> -mcpu=cortex-a55+fp16+rcpc+dotprod
     -march=armv8.2-a+fp16+rcpc+dotprod
     -mtune=cortex-a55
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
  implementer=0x41 part=0xd0b variant=0x4 -> -mcpu=cortex-a76+fp16+rcpc+dotprod
     -march=armv8.2-a+fp16+rcpc+dotprod
     -mtune=cortex-a76
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
  implementer=0x41 part=0xd44 variant=0x1 -> -mcpu=cortex-x1+fp16+rcpc+dotprod+nossbs
     -march=armv8.2-a+fp16+rcpc+dotprod+nossbs
     -mtune=cortex-x1
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
       ssbs (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       PROFILE (omitted because no runtime FEAT_* mapping is available)
```

## Lenovo Legion Y700 (2025) / Qualcomm Snapdragon 8 Gen 3 (Termux)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd80 variant=0x0 : 2 core(s)
  implementer=0x41 part=0xd81 variant=0x0 : 5 core(s)
  implementer=0x41 part=0xd82 variant=0x0 : 1 core(s)

Matched GCC definitions (per observed CPU ID):
  0x41/0xd80 -> -mcpu=cortex-a520
  0x41/0xd81 -> -mcpu=cortex-a720
  0x41/0xd82 -> -mcpu=cortex-x4
  GCC definition: -mcpu=cortex-a520  arch=V9_2A
    FLAGS: SVE2_BITPERM, MEMTAG
  GCC definition: -mcpu=cortex-a720  arch=V9_2A
    FLAGS: SVE2_BITPERM, MEMTAG, PROFILE
  GCC definition: -mcpu=cortex-x4  arch=V9_2A
    FLAGS: SVE2_BITPERM, MEMTAG, PROFILE

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_FLAGM
  + FEAT_FLAGM2
  + FEAT_FP16FML
  + FEAT_DOTPROD
  + FEAT_SM4
  + FEAT_RDM
  + FEAT_LSE
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC
  + FEAT_SHA2
  + FEAT_SHA3
  + FEAT_PMULL
  + FEAT_FP16
  + FEAT_DIT
  + FEAT_DPB
  + FEAT_DPB2
  + FEAT_JSCVT
  + FEAT_FCMA
  + FEAT_RCPC
  + FEAT_RCPC2
  + FEAT_FRINTTS
  + FEAT_I8MM
  + FEAT_BF16
  + FEAT_SB
  + FEAT_BTI

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_CSSC
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SSBS2
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

CPU-matched GCC options with runtime-derived modifiers:
  implementer=0x41 part=0xd80 variant=0x0 -> -mcpu=cortex-a520+nosve+nossbs+nowfxt+nomemtag
     -march=armv9.2-a+nosve+nossbs+nowfxt+nomemtag
     -mtune=cortex-a520
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
       pauth (omitted by including in armv8.3-a)
       rcpc (omitted by including in armv8.3-a)
       fcma (omitted by including in armv8.3-a)
       jscvt (omitted by including in armv8.3-a)
       fp16fml (omitted by including in armv8.4-a)
       dotprod (omitted by including in armv8.4-a)
       flagm (omitted by including in armv8.4-a)
       rcpc2 (omitted by including in armv8.4-a)
       sb (omitted by including in armv8.5-a)
       ssbs (omitted by including in armv8.5-a; runtime feature is unavailable, so +nossbs is emitted)
       predres (omitted by including in armv8.5-a)
       frintts (omitted by including in armv8.5-a)
       flagm2 (omitted by including in armv8.5-a)
       i8mm (omitted by including in armv8.6-a)
       bf16 (omitted by including in armv8.6-a)
       wfxt (omitted by including in armv8.7-a; runtime feature is unavailable, so +nowfxt is emitted)
       xs (omitted by including in armv8.7-a)
       fp16 (omitted by including in armv9-a)
       sve (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2 (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2-bitperm (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       memtag (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
  implementer=0x41 part=0xd81 variant=0x0 -> -mcpu=cortex-a720+nosve+nossbs+nowfxt+nomemtag
     -march=armv9.2-a+nosve+nossbs+nowfxt+nomemtag
     -mtune=cortex-a720
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
       pauth (omitted by including in armv8.3-a)
       rcpc (omitted by including in armv8.3-a)
       fcma (omitted by including in armv8.3-a)
       jscvt (omitted by including in armv8.3-a)
       fp16fml (omitted by including in armv8.4-a)
       dotprod (omitted by including in armv8.4-a)
       flagm (omitted by including in armv8.4-a)
       rcpc2 (omitted by including in armv8.4-a)
       sb (omitted by including in armv8.5-a)
       ssbs (omitted by including in armv8.5-a; runtime feature is unavailable, so +nossbs is emitted)
       predres (omitted by including in armv8.5-a)
       frintts (omitted by including in armv8.5-a)
       flagm2 (omitted by including in armv8.5-a)
       i8mm (omitted by including in armv8.6-a)
       bf16 (omitted by including in armv8.6-a)
       wfxt (omitted by including in armv8.7-a; runtime feature is unavailable, so +nowfxt is emitted)
       xs (omitted by including in armv8.7-a)
       fp16 (omitted by including in armv9-a)
       sve (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2 (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2-bitperm (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       memtag (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       PROFILE (omitted because no runtime FEAT_* mapping is available)
  implementer=0x41 part=0xd82 variant=0x0 -> -mcpu=cortex-x4+nosve+nossbs+nowfxt+nomemtag
     -march=armv9.2-a+nosve+nossbs+nowfxt+nomemtag
     -mtune=cortex-x4
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
       pauth (omitted by including in armv8.3-a)
       rcpc (omitted by including in armv8.3-a)
       fcma (omitted by including in armv8.3-a)
       jscvt (omitted by including in armv8.3-a)
       fp16fml (omitted by including in armv8.4-a)
       dotprod (omitted by including in armv8.4-a)
       flagm (omitted by including in armv8.4-a)
       rcpc2 (omitted by including in armv8.4-a)
       sb (omitted by including in armv8.5-a)
       ssbs (omitted by including in armv8.5-a; runtime feature is unavailable, so +nossbs is emitted)
       predres (omitted by including in armv8.5-a)
       frintts (omitted by including in armv8.5-a)
       flagm2 (omitted by including in armv8.5-a)
       i8mm (omitted by including in armv8.6-a)
       bf16 (omitted by including in armv8.6-a)
       wfxt (omitted by including in armv8.7-a; runtime feature is unavailable, so +nowfxt is emitted)
       xs (omitted by including in armv8.7-a)
       fp16 (omitted by including in armv9-a)
       sve (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2 (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2-bitperm (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       memtag (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       PROFILE (omitted because no runtime FEAT_* mapping is available)
```

## Samsung Galaxy Z Flip 4 / Snapdragon 8+ Gen 1 (Termux)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd46 variant=0x0 : 4 core(s)
  implementer=0x41 part=0xd47 variant=0x2 : 3 core(s)
  implementer=0x41 part=0xd48 variant=0x2 : 1 core(s)

Matched GCC definitions (per observed CPU ID):
  0x41/0xd46 -> -mcpu=cortex-a510
  0x41/0xd47 -> -mcpu=cortex-a710
  0x41/0xd48 -> -mcpu=cortex-x2
  GCC definition: -mcpu=cortex-a510  arch=V9A
    FLAGS: SVE2_BITPERM, MEMTAG, I8MM, BF16
  GCC definition: -mcpu=cortex-a710  arch=V9A
    FLAGS: SVE2_BITPERM, MEMTAG, I8MM, BF16
  GCC definition: -mcpu=cortex-x2  arch=V9A
    FLAGS: SVE2_BITPERM, MEMTAG, I8MM, BF16

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_FLAGM
  + FEAT_FLAGM2
  + FEAT_FP16FML
  + FEAT_DOTPROD
  + FEAT_SM4
  + FEAT_RDM
  + FEAT_LSE
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC
  + FEAT_SHA2
  + FEAT_SHA3
  + FEAT_PMULL
  + FEAT_FP16
  + FEAT_DIT
  + FEAT_DPB
  + FEAT_DPB2
  + FEAT_JSCVT
  + FEAT_FCMA
  + FEAT_RCPC
  + FEAT_RCPC2
  + FEAT_FRINTTS
  + FEAT_I8MM
  + FEAT_BF16
  + FEAT_SB
  + FEAT_BTI

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_CSSC
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SSBS2
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

CPU-matched GCC options with runtime-derived modifiers:
  implementer=0x41 part=0xd46 variant=0x0 -> -mcpu=cortex-a510+i8mm+bf16+nosve+nossbs+nomemtag
     -march=armv9-a+i8mm+bf16+nosve+nossbs+nomemtag
     -mtune=cortex-a510
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
       pauth (omitted by including in armv8.3-a)
       rcpc (omitted by including in armv8.3-a)
       fcma (omitted by including in armv8.3-a)
       jscvt (omitted by including in armv8.3-a)
       fp16fml (omitted by including in armv8.4-a)
       dotprod (omitted by including in armv8.4-a)
       flagm (omitted by including in armv8.4-a)
       rcpc2 (omitted by including in armv8.4-a)
       sb (omitted by including in armv8.5-a)
       ssbs (omitted by including in armv8.5-a; runtime feature is unavailable, so +nossbs is emitted)
       predres (omitted by including in armv8.5-a)
       frintts (omitted by including in armv8.5-a)
       flagm2 (omitted by including in armv8.5-a)
       fp16 (omitted by including in armv9-a)
       sve (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2 (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2-bitperm (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       memtag (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
  implementer=0x41 part=0xd47 variant=0x2 -> -mcpu=cortex-a710+i8mm+bf16+nosve+nossbs+nomemtag
     -march=armv9-a+i8mm+bf16+nosve+nossbs+nomemtag
     -mtune=cortex-a710
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
       pauth (omitted by including in armv8.3-a)
       rcpc (omitted by including in armv8.3-a)
       fcma (omitted by including in armv8.3-a)
       jscvt (omitted by including in armv8.3-a)
       fp16fml (omitted by including in armv8.4-a)
       dotprod (omitted by including in armv8.4-a)
       flagm (omitted by including in armv8.4-a)
       rcpc2 (omitted by including in armv8.4-a)
       sb (omitted by including in armv8.5-a)
       ssbs (omitted by including in armv8.5-a; runtime feature is unavailable, so +nossbs is emitted)
       predres (omitted by including in armv8.5-a)
       frintts (omitted by including in armv8.5-a)
       flagm2 (omitted by including in armv8.5-a)
       fp16 (omitted by including in armv9-a)
       sve (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2 (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2-bitperm (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       memtag (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
  implementer=0x41 part=0xd48 variant=0x2 -> -mcpu=cortex-x2+i8mm+bf16+nosve+nossbs+nomemtag
     -march=armv9-a+i8mm+bf16+nosve+nossbs+nomemtag
     -mtune=cortex-x2
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
       pauth (omitted by including in armv8.3-a)
       rcpc (omitted by including in armv8.3-a)
       fcma (omitted by including in armv8.3-a)
       jscvt (omitted by including in armv8.3-a)
       fp16fml (omitted by including in armv8.4-a)
       dotprod (omitted by including in armv8.4-a)
       flagm (omitted by including in armv8.4-a)
       rcpc2 (omitted by including in armv8.4-a)
       sb (omitted by including in armv8.5-a)
       ssbs (omitted by including in armv8.5-a; runtime feature is unavailable, so +nossbs is emitted)
       predres (omitted by including in armv8.5-a)
       frintts (omitted by including in armv8.5-a)
       flagm2 (omitted by including in armv8.5-a)
       fp16 (omitted by including in armv9-a)
       sve (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2 (omitted by including in armv9-a; runtime feature is unavailable, so +nosve is emitted)
       sve2-bitperm (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)
       memtag (omitted because runtime feature is unavailable; a +no... modifier is emitted instead)

```

## Ulefone Armor 22 / MediaTek Helio G96 (Termux)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x41 part=0xd05 variant=0x1 : 6 core(s)
  implementer=0x41 part=0xd0b variant=0x3 : 2 core(s)

Matched GCC definitions (per observed CPU ID):
  0x41/0xd05 -> -mcpu=cortex-a55
  0x41/0xd0b -> -mcpu=cortex-a76
  GCC definition: -mcpu=cortex-a55  arch=V8_2A
    FLAGS: F16, RCPC, DOTPROD
  GCC definition: -mcpu=cortex-a76  arch=V8_2A
    FLAGS: F16, RCPC, DOTPROD
  GCC definition: -mcpu=cortex-a76.cortex-a55  arch=V8_2A  [BIG.LITTLE]
    FLAGS: F16, RCPC, DOTPROD

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_DOTPROD
  + FEAT_RDM
  + FEAT_LSE
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC
  + FEAT_SHA2
  + FEAT_PMULL
  + FEAT_FP16
  + FEAT_DPB
  + FEAT_RCPC

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_FLAGM
  - FEAT_FLAGM2
  - FEAT_FP16FML
  - FEAT_SM4
  - FEAT_CSSC
  - FEAT_SHA3
  - FEAT_DIT
  - FEAT_DPB2
  - FEAT_JSCVT
  - FEAT_FCMA
  - FEAT_RCPC2
  - FEAT_FRINTTS
  - FEAT_I8MM
  - FEAT_BF16
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SB
  - FEAT_SSBS2
  - FEAT_BTI
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

CPU-matched GCC options with runtime-derived modifiers:
  implementer=0x41 part=0xd05 variant=0x1 -> -mcpu=cortex-a55+fp16+rcpc+dotprod
     -march=armv8.2-a+fp16+rcpc+dotprod
     -mtune=cortex-a55
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
  implementer=0x41 part=0xd0b variant=0x3 -> -mcpu=cortex-a76+fp16+rcpc+dotprod
     -march=armv8.2-a+fp16+rcpc+dotprod
     -mtune=cortex-a76
     omitted feature modifiers (reference; architecture baseline and core-specific omissions):
       fp (omitted by including in armv8-a)
       simd (omitted by including in armv8-a)
       lse (omitted by including in armv8.1-a)
       crc (omitted by including in armv8.1-a)
       rdma (omitted by including in armv8.1-a)
```

## SONY Xperia XZ3 / Qualcomm Snapdragon 845 (Termux)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x51 part=0x803 variant=0x7 : 4 core(s)
  implementer=0x51 part=0x802 variant=0x6 : 4 core(s)

Matched GCC definitions (per observed CPU ID):
  (none)

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_LSE
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC
  + FEAT_SHA2
  + FEAT_PMULL
  + FEAT_FP16

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_FLAGM
  - FEAT_FLAGM2
  - FEAT_FP16FML
  - FEAT_DOTPROD
  - FEAT_SM4
  - FEAT_RDM
  - FEAT_CSSC
  - FEAT_SHA3
  - FEAT_DIT
  - FEAT_DPB
  - FEAT_DPB2
  - FEAT_JSCVT
  - FEAT_FCMA
  - FEAT_RCPC
  - FEAT_RCPC2
  - FEAT_FRINTTS
  - FEAT_I8MM
  - FEAT_BF16
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SB
  - FEAT_SSBS2
  - FEAT_BTI
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

No GCC definition matched any observed implementer/part ID.

GCC-unmatched CPU fallback:
  GCC definition: not found
  FEAT_FP: present
  FEAT_SIMD: present
  fallback -march per observed CPU ID:
    implementer=0x51 part=0x803 variant=0x7 : -march=armv8-a+lse+crc+sha2+aes+fp16 (Qualcomm / Kryo-3XX-Silver)
    implementer=0x51 part=0x802 variant=0x6 : -march=armv8-a+lse+crc+sha2+aes+fp16 (Qualcomm / Kryo-3XX-Gold)
```

## dtab d-41A docomo / Qualcomm Snapdragon 665 (Termux)

```
CPU IDs from /proc/cpuinfo:
  implementer=0x51 part=0x801 variant=0xa : 4 core(s)
  implementer=0x51 part=0x800 variant=0xa : 4 core(s)

Matched GCC definitions (per observed CPU ID):
  (none)

Runtime CPU features detected by upstream cpuinfo.c:
  + FEAT_FP
  + FEAT_SIMD
  + FEAT_CRC
  + FEAT_SHA2
  + FEAT_PMULL

Runtime CPU features NOT detected by upstream cpuinfo.c:
  - FEAT_RNG
  - FEAT_FLAGM
  - FEAT_FLAGM2
  - FEAT_FP16FML
  - FEAT_DOTPROD
  - FEAT_SM4
  - FEAT_RDM
  - FEAT_LSE
  - FEAT_CSSC
  - FEAT_SHA3
  - FEAT_FP16
  - FEAT_DIT
  - FEAT_DPB
  - FEAT_DPB2
  - FEAT_JSCVT
  - FEAT_FCMA
  - FEAT_RCPC
  - FEAT_RCPC2
  - FEAT_FRINTTS
  - FEAT_I8MM
  - FEAT_BF16
  - FEAT_SVE
  - FEAT_SVE_F32MM
  - FEAT_SVE_F64MM
  - FEAT_SVE2
  - FEAT_SVE_PMULL128
  - FEAT_SVE_BITPERM
  - FEAT_SVE_SHA3
  - FEAT_SVE_SM4
  - FEAT_SME
  - FEAT_MEMTAG2
  - FEAT_SB
  - FEAT_SSBS2
  - FEAT_BTI
  - FEAT_WFXT
  - FEAT_SME_F64
  - FEAT_SME_I64
  - FEAT_SME2
  - FEAT_RCPC3
  - FEAT_MOPS

No GCC definition matched any observed implementer/part ID.

GCC-unmatched CPU fallback:
  GCC definition: not found
  FEAT_FP: present
  FEAT_SIMD: present
  fallback -march per observed CPU ID:
    implementer=0x51 part=0x801 variant=0xa : -march=armv8-a+crc+sha2+aes (Qualcomm / Kryo-V2)
    implementer=0x51 part=0x800 variant=0xa : -march=armv8-a+crc+sha2+aes (Qualcomm / Falkor-V1/Kryo)

```

