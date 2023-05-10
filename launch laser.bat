@echo off
pause
:debut
rmdir /s /q test_position
mkdir test_position
cd test_position
for /l %%i in (1,1,9) do (
    mkdir %%i
)
mkdir empty
cd ../
py decoupage_pixel.py
pause
    goto debut