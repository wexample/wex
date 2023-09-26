import datetime

UPGRADE_TYPE_MAJOR = 'major'
UPGRADE_TYPE_INTERMEDIATE = 'intermediate'
UPGRADE_TYPE_MINOR = 'minor'
UPGRADE_TYPE_ALPHA = 'alpha'
UPGRADE_TYPE_BETA = 'beta'
UPGRADE_TYPE_DEV = 'dev'
UPGRADE_TYPE_RC = 'rc'
UPGRADE_TYPE_NIGHTLY = 'nightly'
UPGRADE_TYPE_SNAPSHOT = 'snapshot'

VERSION_PRE_BUILD_NUMBER = 0
VERSION_BUILD_TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
