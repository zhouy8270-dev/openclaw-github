@echo off
echo Checking skills...
echo.

set "TOTAL=0"
set "AVAILABLE=0"
set "MISSING_DEPS=0"
set "BAD_FORMAT=0"

for /d %%d in ("C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\*") do (
    set /a TOTAL+=1
    if not exist "%%d\SKILL.md" (
        set /a BAD_FORMAT+=1
        echo [BAD] %%~nd missing SKILL.md
    )
)

for /d %%d in ("C:\Users\.openclaw\skills\*") do (
    set /a TOTAL+=1
    if not exist "%%d\SKILL.md" (
        set /a BAD_FORMAT+=1
        echo [BAD] %%~nd missing SKILL.md
    )
)

echo.
echo Total: %TOTAL%
echo Available: %AVAILABLE%
echo Missing deps: %MISSING_DEPS%
echo Bad format: %BAD_FORMAT%
