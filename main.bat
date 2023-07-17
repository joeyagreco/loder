@echo off

IF "%1"=="fmt" (
    call scripts\batch\format.bat
) ELSE IF "%1" == "test" (
    call scripts\batch\test.bat
) ELSE (
    echo Invalid flag. Please specify a valid flag.
)
