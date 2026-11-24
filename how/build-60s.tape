Output build.mp4
Set Shell zsh
Set Width 1080
Set Height 1350
Set FontSize 26
Set Padding 30
Set Theme "Catppuccin Mocha"
Set TypingSpeed 25ms
Hide
Type "cd /private/tmp/aaw/game60 && unset CLAUDE_CODE_CHILD_SESSION && clear"
Enter
Type "claude --no-chrome --model opus --setting-sources local --strict-mcp-config --permission-mode acceptEdits --allowedTools Bash Write Edit Read"
Enter
Sleep 8s
Down
Enter
Sleep 5s
Show
Sleep 1s
Type "You have 60 seconds, starting when I press Enter. Make a game I can play in the browser: one file, index.html, keyboard controls. At 60 seconds I stop you and play whatever is in index.html. Go."
Sleep 1s
Enter
Sleep 60s
Ctrl+C
Sleep 300ms
Ctrl+C
Sleep 4s
