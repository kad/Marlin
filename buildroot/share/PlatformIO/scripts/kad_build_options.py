import sys
Import("env")
# print(env.Dump())
print(env['PIOENV'])

tgt = env['PIOENV']
defines = []
if not tgt.startswith("anycubic_mega_zero"):
    print("Error: this script is only for KAD Anycubic Mega Zero build variants", file=sys.stderr)
    exit(1)

parts = tgt.split("_")
model = parts[2]
board = parts[3]
if model not in ('zero', 'zero2'):
    print("Error: unsupported Mega Zero revision", file=sys.stderr)
    exit(1)

if board not in ('melzi', 'btt', 'mks'):
    print("Error: unsupported board", file=sys.stderr)
    exit(1)

board_variant = ""
if board == 'btt':
    board_variant = parts[4]
    # if board_variant == "stdlib":
    #     print("Error: dynamic build parameters expect to work only with nanolib", file=sys.stderr)
    #     exit(1)

ignores = {"anycubic", "mega", "zero", "zero2", "melzi", "btt", "stdlib", "mini", "e3turbo", "mks", "nanov3", "minimal", "dynamic"}
known_tags = {"24v", "zmin", "bed"}
melzi_tags = {"a2", "fs", "sfs"}
btt_tags = {"e0fan"}
e3turbo_tags = {"ubl", "2e", "2to1", "2mix"}
sensors = {"bl", "bltouch", "bfpt", "pinda", "akp"}

for part in parts[4:]:
    print(part)
    if part in ignores or part in known_tags or part in sensors:
        continue
    elif board == "melzi" and part in melzi_tags:
        continue
    elif board == "btt" and part in btt_tags:
        continue
    elif board == "btt" and board_variant == "e3turbo" and part in e3turbo_tags:
        continue
    print("Error: unsupported feature '%s' " % part, file=sys.stderr)
    exit(1)

# PSU 12v/24v. Mega Zero 2 defaults to 24V PSU
if '24v' in parts or model == 'zero2':
    defines.append("-DKAD_PSU_24V")

# Heated bed support. Mega Zero 2 has heated bed by default
if 'bed' in parts or model == 'zero2':
    defines.append("-DKAD_MELZI_BED" if board == 'melzi' else "-DKAD_SKR_BED")

# on BTT SKR E3 Turbo it is possible to have two extruders with different nozzle setups
# 2E - Chimera, independant heaters/nozzles
# 2TO1 - Single nozzle, only one filament possible (Y splitter)
# 2MIX - Single nozzle, mixing two filaments
dual_extruders = [x for x in parts if x in ("2e", "2to1", "2mix")]
if len(dual_extruders) > 1:
    print("Error: only one option for dual extruders supported.", file=sys.stderr)
    exit(1)

if len(dual_extruders) > 0:
    if board_variant == 'e3turbo':
        if "2e" in dual_extruders:
            defines.append("-DKAD_SKR_E3_TURBO_2E")
        elif "2mix" in dual_extruders:
            defines.append("-DKAD_SKR_E3_TURBO_2MIX")
        elif "2to1" in dual_extruders:
            defines.append("-DKAD_SKR_E3_TURBO_2TO1")
    else:
        print("Error: multiple extruders supported only on BTT SKR E3 Tubro board", file=sys.stderr)
        exit(1)

sensors_check = [x for x in parts if x in sensors]
if len(sensors_check) > 1:
    print("Error: only one option for sensor type can be enabled.", file=sys.stderr)
    exit(1)

if sensors.intersection(parts) or "ubl" in parts:
    defines.append("-DKAD_ABL")
    if "ubl" in parts and board == "btt" and board_variant == "e3turbo":
        defines.append("-DKAD_UBL")
    if "zmin" in parts:
        defines.append("-DZ_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN")
    # For now, UBL assumes BLTouch
    if {"bl", "ubl", "bfpt"}.intersection(parts):
        if "bfpt" in parts:
            defines.append("-DKAD_BFPTOUCH")
        else:
            defines.append("-DKAD_BLTOUCH")
        if board == "melzi":
            if "a2" in parts and "zmin" in parts:
                defines.append("-DKAD_MELZI_SERVO_A2")
    elif "pinda" in parts:
        defines.append("-DKAD_PINDA")
        if board == "melzi":
            # Default to PIN27, but potentially can be on EXT-A2
            if "zmin" in parts:
                print("Error: only PIN27 or EXT-A2 can be used for PINDA sensor on Melzi board", file=sys.stderr)
                exit(1)
            elif "a2" in parts:
                defines.append("-DKAD_MELZI_PINDA_A2")
        elif board == "btt":
            if "zmin" in parts:
                print("Error: for PINDA sensor use dedicated sensor port", file=sys.stderr)
                exit(1)
    elif "akp" in parts:
        defines.append("-DKAD_ALLEN_KEY_PROBE")
        if board == "melzi":
            # Default to EXT-A2, but can be used on zmin
            if "zmin" not in parts:
                defines.append("-DKAD_MELZI_AKP_A2")
        elif board == "btt":
            if "zmin" in parts:
                print("Error: for Allen Key Probe use dedicated sensor port", file=sys.stderr)
                exit(1)


# Stock board specific options
if board == "melzi":
    if "fs" in parts:
        defines.append("-DKAD_FILAMENT_SENSOR")
    elif "sfs" in parts:
        defines.append("-DKAD_SMART_FILAMENT_SENSOR")
    if ("fs" in parts or "sfs" in parts) and "a2" in parts and not sensors.intersection(parts):
        defines.append("-DKAD_MELZI_FILAMENT_SENSOR_A2")

# BTT SKR board specific options
if board == "btt":
    if "e0fan" in parts:
        defines.append("-DKAD_SKR_E0_FAN")

if defines:
    env.Append(BUILD_FLAGS=defines)
    # env.Append(CPPDEFINES=defines)
