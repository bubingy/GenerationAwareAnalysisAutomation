if __name__ == '__main__':
    import sys
    
    action = sys.argv[1]

    from utils.init import init_test
    init_test()

    if action == 'download':
        from action import download
        if len(sys.argv) <= 2:           download.download_all()
        else: 
            repo = sys.argv[2]
            if repo == 'runtime':        download.download_runtime()
            elif repo == 'blog-samples': download.download_blog_samples()
            else:                        raise Exception(f'unknown repo: {repo}')
    elif action == 'build':
        from action import build
        if len(sys.argv) <= 2:           build.build_all()
        else:
            repo = sys.argv[2]
            if repo == 'runtime':        build.build_runtime()
            elif repo == 'blog-samples': build.build_genawaredemo()
            else:                        raise Exception(f'unknown repo: {repo}')
    elif action == 'test':
        from action import collect
        from action import analyze
        analyze.install_dotnet_dump()

        dump_root = collect.collect_for_trace_only_scenario()
        analyze.analyze_dump(dump_root)
        dump_root = collect.collect_for_trace_dump_scenario()
        analyze.analyze_dump(dump_root)
        dump_root = collect.collect_for_dump_only_scenario()
        analyze.analyze_dump(dump_root)

        collect.collect_symbols()
    elif action == 'clean':
        from action import clean
        if len(sys.argv) <= 2:           clean.clean_all()
        else: 
            repo = sys.argv[2]
            if repo == 'runtime':        clean.clean_runtime()
            elif repo == 'blog-samples': clean.clean_blog_samples()
            else:                        raise Exception(f'unknown repo: {repo}')
    else:
        raise Exception(f'unknown action: {action}')