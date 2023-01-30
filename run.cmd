@echo off

set WORKDIR=%cd%
set TESTBED=
set RUNTIMECOMMIT=
set BLOGSAMPLESCOMMIT=

call :loadConfig
if %1==download (
    echo downloading runtime
    call :downloadRuntime
    echo downloading blog-samples
    call :downloadBlogSample 
)
if %1==update (
    echo updating runtime
    call :updateRuntime ;
    echo updating blog-samples
    call :updateBlogSample ;;
)
if %1==test (
    echo trace only scenario
    call :generateTraceOnly
    echo trace with dump scenario
    call :generateTraceDump
    echo dump only scenario
    call :generateDumpOnly
) 

:loadConfig 
    FOR /F "tokens=1,2 delims==" %%a in (config) DO (
        if %%a==TestBed (
            %TESTBED%=%%b
        )
        if %%a==RuntimeCommit (
            %RUNTIMECOMMIT%=%%b
        )
        if %%a==BlogSamplesCommit (
            %BLOGSAMPLESCOMMIT%=%%b
        ) 
    ) 
EXIT /B 0

:runCommand
    echo "%~1"
    %~1
EXIT /B 0

:downloadRuntime
    if not exist %TESTBED% (
        mkdir %TESTBED%
    )

    if exist %TESTBED%\runtime (
        echo "runtime already exists!"
        EXIT /B 1
    )

    pushd %TESTBED%
    call :runCommand "git clone https://github.com/dotnet/runtime.git"
    popd
EXIT /B 0

:updateRuntime
    pushd %TESTBED%\runtime
    call :runCommand "git pull"
    call :runCommand "git reset --soft %RUNTIMECOMMIT%"
    popd
EXIT /B 0

:downloadBlogSample
    if not exist %TESTBED% (
        mkdir %TESTBED%
    )

    if exist %TESTBED%\blog-samples (
        echo "blog-samples already exists!"
        EXIT /B 1
    )
    
    pushd %TESTBED%
    call :runCommand "git clone https://github.com/cshung/blog-samples.git"
    popd
EXIT /B 0

:updateBlogSample
    pushd %TESTBED%\blog-samples
    call :runCommand "git pull"
    call :runCommand "git reset --soft %BLOGSAMPLESCOMMIT%"
    popd
EXIT /B 0

:generateTraceOnly
    if not exist %TESTBED%\traceonly (
        mkdir %TESTBED%\traceonly
    )
    pushd %TESTBED%\traceonly
    set COMPlus_GCGenAnalysisGen=1
    set COMPlus_GCGenAnalysisBytes=16E360
    set COMPlus_GCGenAnalysisDump=0
    set COMPlus_GCGenAnalysisTrace=1
    set command=%TESTBED%\runtime\artifacts\tests\coreclr\windows.x64.Checked\Tests\Core_Root\corerun %TESTBED%\blog-samples\GenAwareDemo\bin\Debug\net5.0\GenAwareDemo.dll
    call :runCommand %command%
    popd
EXIT /B 0

:generateTraceDump
    if not exist %TESTBED%\tracedump (
        mkdir %TESTBED%\tracedump
    )
    pushd %TESTBED%\tracedump
    set COMPlus_GCGenAnalysisGen=1
    set COMPlus_GCGenAnalysisBytes=16E360
    set COMPlus_GCGenAnalysisDump=1
    set COMPlus_GCGenAnalysisTrace=1
    set command=%TESTBED%\runtime\artifacts\tests\coreclr\windows.x64.Checked\Tests\Core_Root\corerun %TESTBED%\blog-samples\GenAwareDemo\bin\Debug\net5.0\GenAwareDemo.dll
    call :runCommand %command%
    popd
EXIT /B 0

:generateDumpOnly
    if not exist %TESTBED%\dumponly (
        mkdir %TESTBED%\dumponly
    )
    pushd %TESTBED%\dumponly
    set COMPlus_GCGenAnalysisGen=1
    set COMPlus_GCGenAnalysisBytes=16E360
    set COMPlus_GCGenAnalysisDump=1
    set COMPlus_GCGenAnalysisTrace=0
    set command=%TESTBED%\runtime\artifacts\tests\coreclr\windows.x64.Checked\Tests\Core_Root\corerun %TESTBED%\blog-samples\GenAwareDemo\bin\Debug\net5.0\GenAwareDemo.dll
    call :runCommand %command%
    popd
EXIT /B 0

:collectResult
    if not exist %TESTBED%\TestResult (
        mkdir %TESTBED%\TestResult
    )
    else (
        rd /s/q %TESTBED%\TestResult\*
    )

    move %TESTBED%\traceonly %TESTBED%\TestResult
    move %TESTBED%\tracedump %TESTBED%\TestResult
    move %TESTBED%\dumponly %TESTBED%\TestResult