#!bin/bash

# make executable
pyinstaller AITracker-GUI.spec

# remove compiled binary
directory=$(PWD)
cd dist
rm AITracker-GUI

# create assets folder in the compiled app
cd "AITracker-GUI.app/Contents/MacOS"
mkdir assets
cd "$directory"

# copy assets into the compiled app
cp -R "$directory"/assets/. "dist/AITracker-GUI.app/Contents/MacOS/assets/"

# make a dmg of the application
test -f Application-Installer.dmg && rm Application-Installer.dmg
create-dmg \
  --volname "AITracker-GUI" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "AITracker-GUI.app" 175 120 \
  --hide-extension "AITracker-GUI.app" \
  --app-drop-link 425 120 \
  "AITracker-GUI.dmg" \
  "./dist"