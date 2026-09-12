#!/bin/sh
set -eu
for p in pubspec.yaml codemagic.yaml lib/main.dart assets/questions/questions.json; do
  if [ ! -e "$p" ]; then
    echo "ERROR: Missing $p at repository root."
    echo "Do not upload the ZIP file itself to GitHub. Extract it first, then upload the CONTENTS so pubspec.yaml and codemagic.yaml are visible at the repo root."
    exit 64
  fi
done
echo "Repository layout OK: Flutter files are at the root."
