# Path to Oh My Fish install.
set -gx OMF_PATH "/cygdrive/d/home/.local/share/omf"

# Customize Oh My Fish configuration path.
#set -gx OMF_CONFIG "/cygdrive/d/home/.config/omf"

# Load oh-my-fish configuration.
source $OMF_PATH/init.fish

alias rm "rm -i"
alias grep "grep --color=always -n"
alias less "less -r"
alias global "global --color=always -i"
#function tmux
#    rm -rf /tmp/tmux*;
#    /bin/tmux $argv;
#end

# set env variables
set -g -x SHELL '/usr/bin/fish'

## startup tmux
#if [ $TERM != 'screen' ]
#    tmux
#end
