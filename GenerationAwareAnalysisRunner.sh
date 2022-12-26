WORKDIR=`pwd`
TESTBED=""
RUNTIMECOMMIT=""
BLOGSAMPLESCOMMIT=""

printHelpMessage() {
    # TODO
    echo "help message"
}

loadConfig() {
    while read -r line
    do
        case ${line%:*} in
            TestBed) TESTBED=${line#*:};;
            RuntimeCommit) RUNTIMECOMMIT=${line#*:};;
            BlogSamplesCommit) BLOGSAMPLESCOMMIT=${line#*:};;
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

buildRuntime(){
    pushd $TESTBED/runtime
    runCommand "./build.sh -c checked -s clr"
    runCommand "./build -c release -s libs"
    runCommand "./src/tests/build.sh generatelayoutonly checked"
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

buildBlogSample(){
    pushd $TESTBED/blog-samples/GenAwareDemo
    runCommand "dotnet build"
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
    runCommand "$TESTBED/runtime/artifacts/tests/coreclr/*/Tests/Core_Root/corerun $TESTBED/blog-samples/GenAwareDemo/bin/Debug/net5.0/GenAwareDemo.dll"
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
    runCommand "$TESTBED/runtime/artifacts/tests/coreclr/*/Tests/Core_Root/corerun $TESTBED/blog-samples/GenAwareDemo/bin/Debug/net5.0/GenAwareDemo.dll"
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
    runCommand "$TESTBED/runtime/artifacts/tests/coreclr/*/Tests/Core_Root/corerun $TESTBED/blog-samples/GenAwareDemo/bin/Debug/net5.0/GenAwareDemo.dll"
    popd
}

# case "$1" in
#     help) printHelpMessage ;;

#     download) echo "download" ;
#         case "$2" in
#             -c|--commit) echo "start download";;
#             *)  echo "download dotnet/runtime require commit number specified!"; printHelpMessage; exit 1;;
#         esac ;;

#     build) echo "build" ;;

#     test) ;;
        
#     *) printHelpMessage ;;
# esac
loadConfig
generateDumpOnly
generateTraceDump
generateTraceOnly
# TODO: check before creating directory
# mkdir $TESTBED

# pushd $TESTBED

# popd