WORKDIR=`pwd`
TESTBED=""
RUNTIMECOMMIT=""
BLOGSAMPLESCOMMIT=""

HELPMESSAGE="
./GenerationAwareAnalysisRunner.sh <action>
action:
    download - clone the latest source to local
    update - retrieve update from github
    test - run the test
"

printHelpMessage() {
    # TODO
    echo "help message"
}

loadConfig() {
    while read -r line
    do
        case ${line%=*} in
            TestBed) TESTBED=${line#*=};;
            RuntimeCommit) RUNTIMECOMMIT=${line#*=};;
            BlogSamplesCommit) BLOGSAMPLESCOMMIT=${line#*=};;
        esac
    done < $WORKDIR/config
}

runCommand() {
    echo "run command: " $1
    $1
}

downloadRuntime() {
    if [ ! -d $TESTBED ]; then 
        mkdir $TESTBED
    fi

    if [ -d $TESTBED/runtime ]; then 
        echo "runtime already exists!"
        exit 1
    fi

    pushd $TESTBED
    runCommand "git clone https://github.com/dotnet/runtime.git"
    popd
}

updateRuntime() {
    pushd $TESTBED/runtime
    runCommand "git pull"
    runCommand "git reset --soft $RUNTIMECOMMIT"
    popd
}

downloadBlogSample() {
    if [ ! -d $TESTBED ]; then 
        mkdir $TESTBED
    fi

    if [ -d $TESTBED/blog-samples ]; then 
        echo "blog-samples already exists!"
        exit 1
    fi

    pushd $TESTBED
    runCommand "git clone https://github.com/cshung/blog-samples.git"
    popd
}

updateBlogSample() {
    pushd $TESTBED/blog-samples
    runCommand "git pull"
    runCommand "git reset --soft $BLOGSAMPLESCOMMIT"
    popd
}

generateTraceOnly() {
    if [ ! -d $TESTBED/traceonly ]; then 
        mkdir $TESTBED/traceonly
    fi
    pushd $TESTBED/traceonly
    export COMPlus_GCGenAnalysisGen=1
    export COMPlus_GCGenAnalysisBytes=16E360
    export COMPlus_GCGenAnalysisDump=0
    export COMPlus_GCGenAnalysisTrace=1
    runCommand "$TESTBED/runtime/artifacts/tests/coreclr/*/Tests/Core_Root/corerun $TESTBED/blog-samples/GenAwareDemo/bin/Debug/*/GenAwareDemo.dll"
    popd
}

generateTraceDump() {
    if [ ! -d $TESTBED/tracedump ]; then 
        mkdir $TESTBED/tracedump
    fi
    pushd $TESTBED/tracedump
    export COMPlus_GCGenAnalysisGen=1
    export COMPlus_GCGenAnalysisBytes=16E360
    export COMPlus_GCGenAnalysisDump=1
    export COMPlus_GCGenAnalysisTrace=1
    runCommand "$TESTBED/runtime/artifacts/tests/coreclr/*/Tests/Core_Root/corerun $TESTBED/blog-samples/GenAwareDemo/bin/Debug/*/GenAwareDemo.dll"
    popd
}

generateDumpOnly() {
    if [ ! -d $TESTBED/dumponly ]; then 
        mkdir $TESTBED/dumponly
    fi
    pushd $TESTBED/dumponly
    export COMPlus_GCGenAnalysisGen=1
    export COMPlus_GCGenAnalysisBytes=16E360
    export COMPlus_GCGenAnalysisDump=1
    export COMPlus_GCGenAnalysisTrace=0
    runCommand "$TESTBED/runtime/artifacts/tests/coreclr/*/Tests/Core_Root/corerun $TESTBED/blog-samples/GenAwareDemo/bin/Debug/*/GenAwareDemo.dll"
    popd
}

collectResult() {
    if [ ! -d $TESTBED/TestResult ]; then 
        mkdir $TESTBED/TestResult
    else
        rm -rf $TESTBED/TestResult/*
    fi

    mv $TESTBED/traceonly $TESTBED/TestResult
    mv $TESTBED/tracedump $TESTBED/TestResult
    mv $TESTBED/dumponly $TESTBED/TestResult
}

##################
## MAIN PROCESS ##
##################
loadConfig
case "$1" in
    help) printHelpMessage ;;

    download) 
        echo "downloading runtime" ;
        downloadRuntime ;
        echo "downloading blog-samples" ;
        downloadBlogSample ;;

    update)
        echo "updating runtime" ;
        updateRuntime ;
        echo "updating blog-samples" ;
        updateBlogSample ;;

    test) 
        echo "trace only scenario" ; generateTraceOnly ;
        echo "trace & dump scenario" ; generateTraceDump ;
        echo "dump only scenario" ; generateDumpOnly ;
        echo "collect result" ; collectResult ;;
        
    *) printHelpMessage ;;
esac
