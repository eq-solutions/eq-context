@echo off
echo Removing orphan Claude worktrees...

rd /s /q "C:\Projects\eq-context\.claude\worktrees\practical-bhabha-e28313"
rd /s /q "C:\Projects\eq-solves-field\.claude\worktrees\dreamy-bhabha-006b91"
rd /s /q "C:\Projects\eq-solves-field\.claude\worktrees\epic-noether-984c57"
rd /s /q "C:\Projects\eq-solves-field\.claude\worktrees\festive-roentgen-60761d"
rd /s /q "C:\Projects\eq-solves-field\.claude\worktrees\loving-dubinsky-128a63"
rd /s /q "C:\Projects\eq-solves-field\.claude\worktrees\upbeat-varahamihira-797063"
rd /s /q "C:\Projects\eq-solves-field\.claude\worktrees\zen-golick-a9e7e1"
rd /s /q "C:\Projects\eq-solves-service\.claude\worktrees\crazy-swanson-cb5a62"
rd /s /q "C:\Projects\eq-solves-service\.claude\worktrees\relaxed-hopper-e45f17"
rd /s /q "C:\Projects\eq-solves-service\.claude\worktrees\sharp-germain-af2e3f"
rd /s /q "C:\Projects\eq-solves-service\.claude\worktrees\xenodochial-clarke-fe01e2"

echo Done. Errors above mean the folder was already gone.
pause
