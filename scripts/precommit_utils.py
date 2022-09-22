import sys
import os


def interpret_precommit_args():
    """Precommit passes its arguments strangely and this lets us figure out which ones are which type"""
    cli_args = []
    path_args = []
    for arg in sys.argv[1:]:
        if os.path.exists(arg):
            path_args.append(arg)
        else:
            cli_args.append(arg)

    if not path_args:
        raise Exception(
            f"Everything passed was considered to be a CLI argument, so there was nothing to check. {cli_args}"
        )


    return path_args, cli_args
