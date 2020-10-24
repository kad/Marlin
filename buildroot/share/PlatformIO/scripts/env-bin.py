Import("env")

if 'MARLIN_FEATURES' in env and 'SHORT_BUILD_VERSION' in env['MARLIN_FEATURES']:
    env.Replace(PROGNAME="%s-%s-firmware" % (env['PIOENV'], env['MARLIN_FEATURES']['SHORT_BUILD_VERSION'].strip('"')))
else:
    env.Replace(PROGNAME="%s-firmware" % (env['PIOENV'],))
