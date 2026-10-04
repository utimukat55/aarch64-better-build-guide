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

## Google Pixel 6a (Termux)

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

