if __name__ == '__main__':
    import os
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
    elif action == 'update':
        from action import update
        if len(sys.argv) <= 2:           update.update_all()
        else: 
            repo = sys.argv[2]
            if repo == 'runtime':        update.update_runtime()
            elif repo == 'blog-samples': update.update_blog_samples()
            else:                        raise Exception(f'unknown repo: {repo}')
    elif action == 'test':
        from action import test
        test.test_trace_only_scenario()
        test.test_trace_dump_scenario()
        test.test_dump_only_scenario()
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