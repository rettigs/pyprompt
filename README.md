Your own shell prompt, but written in Python!

Also condenses the cwd, current git branch, and virtualenv when your window is tiny to give you some extra typing room.

To use, clone this repo:
```
cd
git clone git@github.com:rettigs/pyprompt.git
```
Then put this in your `~/.bashrc`: (if you're using bash)
```
PROMPT_COMMAND=set_prompt
set_prompt () {
    export PS1="$(~/pyprompt/prompt.py)"
}
```
