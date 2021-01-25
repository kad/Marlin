Import("env")

prefix = env['PIOENV']
if prefix.startswith("anycubic_mega_zero"):
    prefix = prefix.replace("anycubic_mega_zero", "amz", 1)

if 'MARLIN_FEATURES' in env and 'SHORT_BUILD_VERSION' in env['MARLIN_FEATURES']:
    build_version = env['MARLIN_FEATURES']['SHORT_BUILD_VERSION'].strip('"')
    if build_version == "bugfix-2.0.x" and 'STRING_DISTRIBUTION_DATE' in env['MARLIN_FEATURES']:
        build_version = build_version + "-" + env['MARLIN_FEATURES']['STRING_DISTRIBUTION_DATE'].strip('"').replace("-","")
    env.Replace(PROGNAME="%s-%s-firmware" % (prefix, build_version))
else:
    env.Replace(PROGNAME="%s-firmware" % (prefix,))
