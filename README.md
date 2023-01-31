# GenerationAwareAnalysisAutomation
## Introduction
This script can be used to download, update and clean dotnet/runtime and cshung/blog-samples to specific directory. It also facilitate trace and dump collection.

## Usage
1. Configuration  
Open `run.conf` in project root, specify commit number of dotnet/runtime and cshung/blog-samples separately. Then set `testbed`, where dotnet/runtime and cshung/blog-samples located.

2. Run  
Windows:  
```python main.py <action> <option>```  
Linux and Mac:  
```python3 main.py <action> <option>```  
`<action>` can be `download`, `update`, `clean` or `test`  

* download  
Running ```python main.py download``` downloads dotnet/runtime and cshung/blog-samples.  
Running ```python main.py download runtime``` downloads dotnet/runtime only.  
Running ```python main.py download blog-samples``` downloads cshung/blog-samples only.

* update  
Running ```python main.py update``` updates dotnet/runtime and cshung/blog-samples.  
Running ```python main.py update runtime``` updates dotnet/runtime only.  
Running ```python main.py update blog-samples``` updates cshung/blog-samples only.

* clean  
Running ```python main.py clean``` cleans dotnet/runtime and cshung/blog-samples.  
Running ```python main.py clean runtime``` cleans dotnet/runtime only.  
Running ```python main.py clean blog-samples``` cleans cshung/blog-samples only.

* test  
Running ```python main.py test``` to perform test in trace-only, dump-only, trace&dump scenarios separately. Trace and dump files are stored in `testbed`/TestResult.