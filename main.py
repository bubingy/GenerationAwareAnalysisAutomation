if __name__ == '__main__':
    import os
    import sys
    
    action = sys.argv[1]

    from utils.config_load import load_config
    load_config(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            'run.config'
        )
    )

    if action == 'download':
        from action import download
        repo = sys.argv[2]
        if repo == '' or repo is None: download.download_all()
        elif repo == 'runtime':        download.download_runtime()
        elif repo == 'blog-samples':   download.download_blog_samples()
        else:                          raise Exception(f'unknown repo: {repo}')
    elif action == 'update':
        from action import update
        repo = sys.argv[2]
        if repo == '' or repo is None: update.update_all()
        elif repo == 'runtime':        update.update_runtime()
        elif repo == 'blog-samples':   update.update_blog_samples()
        else:                          raise Exception(f'unknown repo: {repo}')
    elif action == 'test':
        pass
    elif action == 'clean':
        from action import clean
        repo = sys.argv[2]
        if repo == '' or repo is None: clean.clean_all()
        elif repo == 'runtime':        clean.clean_runtime()
        elif repo == 'blog-samples':   clean.clean_blog_samples()
        else:                          raise Exception(f'unknown repo: {repo}')
    else:
        raise Exception(f'unknown action: {action}')