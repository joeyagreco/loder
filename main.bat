@echo off

IF "%1"=="fmt" (
    call scripts\batch\format.bat
) ELSE (
    echo Invalid flag. Please specify a valid flag.
)
