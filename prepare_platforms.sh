#!/bin/sh
set -eu
if [ ! -d android ] || [ ! -d ios ]; then
  flutter create --no-pub --platforms=android,ios --org com.privatewellness --project-name trans_wellness_private .
fi
# image_picker 1.2.x supports Android API 24+ and iOS 13+.
if [ -f android/app/src/main/AndroidManifest.xml ] && ! grep -q 'android.permission.INTERNET' android/app/src/main/AndroidManifest.xml; then
  sed -i.bak '0,/<manifest/{s#<manifest#<manifest#}' android/app/src/main/AndroidManifest.xml || true
  python3 - <<'PY2'
from pathlib import Path
p=Path('android/app/src/main/AndroidManifest.xml')
s=p.read_text()
if 'android.permission.INTERNET' not in s:
    marker='>'
    i=s.find(marker)
    if i != -1:
        s=s[:i+1]+'\n    <uses-permission android:name="android.permission.INTERNET" />'+s[i+1:]
        p.write_text(s)
PY2
fi
if [ -f android/app/build.gradle.kts ]; then
  sed -i.bak 's/minSdk = flutter.minSdkVersion/minSdk = 24/' android/app/build.gradle.kts || true
fi
if [ -f android/app/build.gradle ]; then
  sed -i.bak 's/minSdkVersion flutter.minSdkVersion/minSdkVersion 24/' android/app/build.gradle || true
fi
if [ -f ios/Podfile ]; then
  sed -i.bak "s/# platform :ios, '.*'/platform :ios, '13.0'/" ios/Podfile || true
fi
if [ -f ios/Runner/Info.plist ]; then
  /usr/libexec/PlistBuddy -c "Set :NSPhotoLibraryUsageDescription Private progress photos are only selected when you choose to add one." ios/Runner/Info.plist 2>/dev/null || \
  /usr/libexec/PlistBuddy -c "Add :NSPhotoLibraryUsageDescription string Private progress photos are only selected when you choose to add one." ios/Runner/Info.plist
  /usr/libexec/PlistBuddy -c "Set :NSCameraUsageDescription The camera is used only when you choose to take a private progress photo." ios/Runner/Info.plist 2>/dev/null || \
  /usr/libexec/PlistBuddy -c "Add :NSCameraUsageDescription string The camera is used only when you choose to take a private progress photo." ios/Runner/Info.plist
fi
