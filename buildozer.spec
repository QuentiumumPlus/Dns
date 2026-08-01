[app]

# App metadata
title = KiwiBypass
package.name = kiwibypass
package.domain = org.kiwi

# Android build settings
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json
source.include_patterns = *
source.exclude_patterns = .buildozer,.git,build,dist

version = 1.0.0

# Requirements
# KivyMD 2.0.1 PyPI'de yok - GitHub master'dan cekilir
requirements = python3,kivy==2.3.1,cython==3.0.11,kivymd==https://github.com/kivymd/KivyMD/archive/master.zip

# Android specifics
orientation = portrait
fullscreen = 1

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# Android architecture
android.archs = arm64-v8a

# App icon (optional - if missing, default is used)
icon.filename = %(source.dir)s/icon.png

# Presplash color
android.presplash_color = #0A0A0F

# Debug mode
android.debug = 0

# Services
services = 

# Frameworks
android.api = 33
android.minapi = 21
android.ndk_api = 21

[buildozer]

log_level = 2
warn_on_root = 1
