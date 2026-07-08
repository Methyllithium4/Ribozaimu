#!/bin/bash

kwriteconfig6 --file kwinrc --group Plugins --key zaimu_bridgeEnabled true

kpackagetool6 --type KWin/Script -i .
kpackagetool6 --type KWin/Script -r zaimu_bridge
kpackagetool6 --type KWin/Script -i .
