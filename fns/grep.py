
import argparse
from pathlib import Path
import sys
import traceback
import regex as rx

###########################################
rxp = {
    'xx': "ssss",
}

###########################################
def repl(x):
    try:
        nm, v = [(g, v) for g, v in x.groupdict().items() if v != None and not g.startswith('_')][0]
    except:
        traceback.print_exc()
        print(x.groupdict())
        sys.exit(7)

    # return '\033[1;31m' + x.group() + '\033[0m'
    return '\033[1;31m' + (v if nm == 'xx' else f'({nm}){v}') + '\033[0m'

###########################################
def main(rexp, path):
    # print(rexp, '\n', path)
    rexp = '|'.join([f'(?P<{nm}>{r})' for nm, r in (rxp.items() if rexp == '@@@' else {'xx': rexp}.items())])

    pt = rx.compile(rexp, flags=rx.I|rx.M)
    
    for p in path:
        with open(p, 'r', encoding='utf-8') as f:
            for ii, line in enumerate(f, 1):
                v = pt.sub(repl, line)
                if '[0m' in v:
                    print(f'{Path(f.name).name}: {ii}: {v}', end='')

###########################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('rexp')
    parser.add_argument('path', nargs='*')
    args = parser.parse_args()
    main(args.rexp, args.path)
    