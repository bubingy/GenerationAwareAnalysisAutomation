import os
import sys

import app
from configuration import GenerationAwareAnalyzeConfiguration

if __name__ == '__main__':
    
    
    action = sys.argv[1]
    conf_path = os.path.join(app.script_root, 'run.conf')
    test_conf = GenerationAwareAnalyzeConfiguration(conf_path)

    if action == 'download':
        from actions import download
        if len(sys.argv) <= 2:
            download.download_runtime(test_conf)
            download.download_blog_samples(test_conf)
        else: 
            repo = sys.argv[2]
            if repo == 'runtime':
                download.download_runtime()
            elif repo == 'blog-samples':
                download.download_blog_samples()
            else:
                raise Exception(f'unknown repo: {repo}')
    elif action == 'build':
        from actions import target_app
        if len(sys.argv) <= 2:
            target_app.build_runtime(test_conf)
            target_app.build_genawaredemo(test_conf)
        else:
            repo = sys.argv[2]
            if repo == 'runtime':
                target_app.build_runtime(test_conf)
            elif repo == 'blog-samples':
                target_app.build_genawaredemo(test_conf)
            else:
                raise Exception(f'unknown repo: {repo}')
    elif action == 'test':
        from actions import collect
        from actions import analyze

        collect.set_registry_keys(test_conf)
        
        analyze.install_dotnet_dump()

        dump_root = collect.collect_for_trace_only_scenario(test_conf)
        analyze.analyze_dump(dump_root)
        dump_root = collect.collect_for_trace_dump_scenario(test_conf)
        analyze.analyze_dump(dump_root)
        dump_root = collect.collect_for_dump_only_scenario(test_conf)
        analyze.analyze_dump(dump_root)

        collect.collect_symbols()

    elif action == 'clean':
        from actions import clean
        clean.remove_dotnet_temp(test_conf)
        clean.remove_registry_keys(test_conf)
    else:
        raise Exception(f'unknown action: {action}')