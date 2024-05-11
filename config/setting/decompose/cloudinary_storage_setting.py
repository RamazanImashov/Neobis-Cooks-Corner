from decouple import config

CLOUDINARY_STORAGE_SETTING = {
    "CLOUD_NAME": config("CLOUD_NAME"),
    "API_KEY": config("API_KEY"), 
    "API_SECRET": config("API_SECRET"),
}