[app]

# App info
title = SalesApp
package.name = salesapp
package.domain = org.dnbrunovic
source.dir = .
source.main = sales.py
version = 1.0
orientation = portrait
fullscreen = 1

# Modules your app uses
requirements = python==3.10,kivy==2.0.0,https://github.com/kivymd/KivyMD/archive/master.zip,sdl2_ttf==2.0.15,pillow

# Include additional files
include_patterns = *.db, *.kv, images/*.png, images/*.jpg, *.env

# Permissions for file and internet access
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Target Android architectures
android.archs = armeabi-v7a, arm64-v8a
android.use_setup_py = 1

# Minimum and target Android APIs
android.minapi = 30
android.target = 30
android.extra_cflags = -Wno-macro-redefined

# Optional: use NDK 25b if you hit NDK issues
android.ndk = 25b

# SDK path if sdkmanager is missing
#android.sdk_path = 

# Logging level
log_level = 1

# Keep build cache for faster rebuilds
android.keep_build_dir = 1

# Copy APK to bin/ directory
copy_to_bin = 1


[buildozer]

# Log level
log_level = 1

# Warn if run as root
warn_on_root = 1