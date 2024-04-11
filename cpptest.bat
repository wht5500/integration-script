@echo on

set STATIC_Rule="builtin://MISRA C 2012"
set CPPTEST_INSTALL_PATH="C:\Program Files\parasoft_cpptest_professional-2022.1.0-win32.x86_64\cpptest\bin\engine\etc\compilers"
set root_path=%~dp0

xcopy /y /i /d %root_path%\segarmgcc_7 %CPPTEST_INSTALL_PATH%\segarmgcc_7

:: Code static analysis boot start
set build_path=%root_path%..\..\..\Boot\Build\SES
cd %build_path%
copy /y /b %root_path%\build_boot.bat  %build_path%\build.bat

if exist "%root_path%\workspace" (
    del /s /q "%root_path%\workspace"
)
if exist "%root_path%\mcu.bdf" (
    del /s /q "%root_path%\mcu.bdf"
)

::del /s /q %build_path%\Output\Debug\Obj\sf\*.*
cpptesttrace --cpptesttraceOutputFile=%root_path%\mcu.bdf --cpptesttraceTraceCommand="cc1|ld" --cpptesttraceProjectName=mcu "build.bat "
::del /s /q %build_path%\Output\Debug\Obj\sf\*.*
cpptestcli -exclude **/AutoSar/BSW/** -exclude **/AutoSar/Config/** -exclude **/AutoSar/MCAL/** -bdf "%root_path%\mcu.bdf"  -config %STATIC_Rule% -showdetails -data "%root_path%\workspace" -report %root_path%\boot_report.html -settings %root_path%\compiler.txt
:: Code static analysis boot end

:: Code static analysis sx0 start
set build_path=%root_path%..\..\Build\sx0\SES
cd %build_path%
copy /y /b %root_path%\build_sx0.bat  %build_path%\build.bat

if exist "%root_path%\workspace" (
    del /s /q "%root_path%\workspace"
)
if exist "%root_path%\mcu.bdf" (
    del /s /q "%root_path%\mcu.bdf"
)


:: Code static analysis sf end


pause
