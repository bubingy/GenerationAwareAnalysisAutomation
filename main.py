if __name__ == '__main__':
    import os
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument(
        'action',
        choices=['download', 'update', 'test', 'clean'])
    args = parse.parse_args()

    from utils.config_load import load_config
    load_config(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            'run.config'
        )
    )

    if args.action == 'download':
        pass
    if args.action == 'update':
        pass
    if args.action == 'test':
        pass
    if args.action == 'clean':
        pass