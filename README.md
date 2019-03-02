# [GitHunk](//packagecontro.io/packages/GitHunk)

This is a _work in progress_ plugin that extends the inline diff feature added to Sublime Text in build 3193.

It will allow you to enter a "hunk staging mode" for the currently focused view.
In this mode the view is read-only, and has a custom set of key bindings:

- `n` to go to next hunk
- `p` to go to prev hunk
- `h` to stage current hunk
- `d` to discard (revert) current hunk
- `?` to toggle help text
- `escape` to exit mode

Currently the staging isn't implemented.

#### TODO

- Fix staging
- Can we recolor the selection of an inserted hunk?
	- When the cursor is not selecting the insert in the hunk, the inserted part is green,
	  but when we select it it's theme-default (blue)
- Find a way to display to the user that they're in "staging mode"

## Options

Users can override the options in `Packages/User/GitHunk.sublime-settings`.

This file can be opened either through the menus (_Preferences_ > _Package Settings_ > _GitHunk_ > _Settings_) or through the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Preferences: GitHunk Settings`.

Users can also override the keybindings in `Packages/User/Default.sublime-keymap`.

This file can be opened either through the menus (_Preferences_ > _Package Settings_ > _GitHunk_ > _Key Bindings_) or through the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Preferences: GitHunk Key Bindings`.

## Installation

##### Using the package manager

1. Install the [Sublime Text Package Control](//packagecontrol.io/installation) plugin if you haven't already.
    - _Preferences_ > _Package Control_
2. Open up the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Package Control: Install Package`
3. Search for `GitHunk` and hit <kbd>Enter</kbd> to install.

##### Manual installation with Git

1. Click the `Preferences > Browse Packages` menu.
2. Open up a terminal and execute the following:
    - `git clone https://github.com/p3lim/sublime-githunk GitHunk`
3. Restart Sublime Text.
