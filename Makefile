COMMON_CONF = apache-credit

CREDIT_ANCHORTEXT = PunBB Appliance
define CREDIT_STYLE_EXTRA
#turnkey-credit { clear: both; }
#turnkey-credit > div { width: 100%; text-align: center; }
endef

include $(FAB_PATH)/common/mk/turnkey/lamp.mk
include $(FAB_PATH)/common/mk/turnkey.mk
