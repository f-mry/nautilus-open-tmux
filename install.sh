#!/bin/env sh

if [[ -d $HOME/.local/share/nautilus-python ]]; then
    cp ./tmux-open.py $HOME/.local/share/nautilus-python/extensions/tmux-open.py
    nautilus -q
    echo "Installed"
else
    mkdir -p $HOME/.local/share/nautilus-python
    cp ./tmux-open.py $HOME/.local/share/nautilus-python/extensions/tmux-open.py
    nautilus -q
    echo "Installed"
fi
    
