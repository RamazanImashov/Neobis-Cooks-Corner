__all__ = (
    "ADMIN_APPS",
    "BASE_APPS",
    "LIBS_APPS",
    "APPS",
    "BM",
    "TS",
    "APVS",
    "JBS",
    "RF_BS",
    "JWT_BS",
    "SP_BS",
    "LOG_BS",
    "CLOUD_STORAGE_SETTING"
)

from config.setting.decompose.installed_apps_setting import ADMIN_APPS, BASE_APPS, LIBS_APPS, APPS
from config.setting.decompose.middleware_setting import BASE_MIDDLEWARE as BM
from config.setting.decompose.templates_setting import BASE_SETTING as TS
from config.setting.decompose.auth_password_validators_setting import BASE_SETTING as APVS
from config.setting.decompose.jazzmin_setting import BASE_SETTINGS as JBS
from config.setting.decompose.rest_framework_setting import BASE_SETTING as RF_BS
from config.setting.decompose.jwt_setting import BASE_SETTING as JWT_BS
from config.setting.decompose.spectacular import BASE_SETTINGS as SP_BS
from config.setting.decompose.logging_setting import BASE_SETTING as LOG_BS
from config.setting.decompose.cloudinary_storage_setting import CLOUDINARY_STORAGE_SETTING as CLOUD_STORAGE_SETTING
