cmake_minimum_required(VERSION 3.20)
project(aarch64-better-build-guide LANGUAGES C CXX)

enable_testing()

if(NOT CMAKE_SYSTEM_PROCESSOR MATCHES "^(aarch64|AARCH64)$")
  message(WARNING "This program is intended to run/build natively on AArch64. It can still be configured elsewhere for inspection.")
endif()

set(UPSTREAM ${CMAKE_CURRENT_SOURCE_DIR}/upstream/gcc)
set(UP_A64 ${UPSTREAM}/config/aarch64)
set(UP_CPUINFO ${UPSTREAM}/common/config/aarch64)
set(UP_LIBGCC ${UPSTREAM}/libgcc/config/aarch64)
set(GEN ${CMAKE_CURRENT_BINARY_DIR}/generated)
file(MAKE_DIRECTORY ${GEN})
find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(INPUT_CORES ${UP_A64}/aarch64-cores.def)
set(INPUT_ARCHES ${UP_A64}/aarch64-arches.def)
set(INPUT_EXT   ${UP_A64}/aarch64-option-extensions.def)
set(INPUT_DEPS  ${UP_A64}/aarch64-feature-deps.h)
set(INPUT_CPUH  ${UP_CPUINFO}/cpuinfo.h)
set(INPUT_CPUC  ${UP_LIBGCC}/cpuinfo.c)
set(INPUT_LSCPU ${CMAKE_CURRENT_SOURCE_DIR}/upstream/util-linux/sys-utils/lscpu-arm.c)

add_custom_command(
  OUTPUT ${GEN}/core_table.inc ${GEN}/feature_table.inc ${GEN}/flag_table.inc ${GEN}/architecture_table.inc ${GEN}/lscpu_table.inc
  COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tools/generate_tables.py
          --cores ${INPUT_CORES}
          --arches ${INPUT_ARCHES}
          --cpuinfo-h ${INPUT_CPUH}
          --option-extensions ${INPUT_EXT}
          --feature-deps-h ${INPUT_DEPS}
          --lscpu-arm ${INPUT_LSCPU}
          --out-dir ${GEN}
  DEPENDS ${INPUT_CORES} ${INPUT_ARCHES} ${INPUT_CPUH} ${INPUT_CPUC} ${INPUT_A64CC} ${INPUT_EXT} ${INPUT_DEPS} ${INPUT_LSCPU}
          ${CMAKE_CURRENT_SOURCE_DIR}/tools/generate_tables.py
  VERBATIM)
add_custom_target(generated_tables DEPENDS ${GEN}/core_table.inc ${GEN}/feature_table.inc ${GEN}/flag_table.inc ${GEN}/architecture_table.inc ${GEN}/lscpu_table.inc)

# リンカオプションに --allow-multiple-definition を追加
if(ANDROID)
    add_link_options(-Wl,--allow-multiple-definition)
endif()

add_executable(aarch64-better-build-guide
  src/main.cpp
  src/native_cpu_features.c
  ${INPUT_CPUC}
  ${GEN}/core_table.inc
  ${GEN}/feature_table.inc
  ${GEN}/flag_table.inc
  ${GEN}/architecture_table.inc
  ${GEN}/lscpu_table.inc)
add_dependencies(aarch64-better-build-guide generated_tables)
target_include_directories(aarch64-better-build-guide PRIVATE ${UPSTREAM} ${GEN})
target_compile_features(aarch64-better-build-guide PRIVATE cxx_std_17)

install(TARGETS aarch64-better-build-guide RUNTIME DESTINATION bin)

add_test(NAME parser
  COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tools/test_parser.py)

add_test(NAME fallback_qcom
  COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tools/test_fallback.py
          $<TARGET_FILE:aarch64-better-build-guide>
          ${GEN}/feature_table.inc
          ${CMAKE_CURRENT_SOURCE_DIR}/tests/qcom.cpuinfo)

# リンカオプションに --allow-multiple-definition を追加
if(ANDROID)
    add_link_options(-Wl,--allow-multiple-definition)
endif()
