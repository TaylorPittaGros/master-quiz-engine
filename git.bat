@echo off
cd /d "%~dp0"

git add .

git diff --cached --quiet
IF %ERRORLEVEL% EQU 0 (
    echo ❌ Nothing changed.
) ELSE (
    git commit -m "Auto update"
    git push
    echo ✅ Code pushed to GitHub!
)

pause