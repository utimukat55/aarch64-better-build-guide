/* aarch64 better build guide
   Copyright (C) 2026 utimukat55

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdint.h>
#include <stdlib.h>

#include "common/config/aarch64/cpuinfo.h"

/* cpuinfo.c owns this GCC runtime structure. Keep this declaration compatible
   with the definition in the upstream file; the program only reads it after
   the constructor has initialized it. */
extern struct {
  unsigned long long features;
} __aarch64_cpu_features;

uint64_t native_cpu_feature_mask(void)
{
  const char *override = getenv("AARCH64_NATIVE_MCPU_FEATURE_MASK");
  if (override && *override) return (uint64_t)strtoull(override, NULL, 0);
  return __atomic_load_n(&__aarch64_cpu_features.features, __ATOMIC_RELAXED);
}
