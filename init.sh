#!/usr/bin/env bash
# AGON shell init — source this in ~/.bashrc or ~/.zshrc
# Usage: echo "source /path/to/agon/init.sh" >> ~/.bashrc
#
# On every terminal start:
#   - Checks Hermes + AGON are installed
#   - Shows AGON banner
#   - Sets HERMES_SKIN=agon env var

AGON_ROOT="$(cd "$(dirname "$BASH_SOURCE")" && pwd 2>/dev/null || echo ".")"

if command -v hermes &>/dev/null; then
    # Ensure AGON is default personality
    hermes config set agent.default_personality agon 2>/dev/null || true

    # Skin is applied via agon command or chat.sh
    export HERMES_SKIN="agon" 2>/dev/null || true

    # Show banner (first terminal start only)
    if [ -z "$AGON_INIT_DONE" ]; then
        echo -e "\033[0;36m  ⚔ AGON — daimon of contest. 82 minds. One blade.\033[0m"
        echo -e "\033[0;36m  hermes chat  |  ./agon  |  ./chat.sh\033[0m"
        echo ""
        export AGON_INIT_DONE=1
    fi
fi
