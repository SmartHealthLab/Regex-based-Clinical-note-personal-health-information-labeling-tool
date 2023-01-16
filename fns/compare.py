import argparse
import difflib
from pathlib import Path
import sys

###########################################
def dir_compare(dold, dnew):
    fsold = [x.stem for x in Path(dold).glob('*')]
    fsnew = [x.stem for x in Path(dnew).glob('*')]

    for x in ['old', 'new']:
        fs = fsold if x == 'old' else fsnew
        for f in sorted(fs):
            if f.name not in [f2.name for f2 in (fsnew if x == 'old' else fsold)]:
                print(f'{x} only: {f.name}')

###########################################
def file_compare(fold, fnew):

    if not fold.exists() or not fnew.exists():
        print('exists:', fold.exists(), ':', fold)
        print('exists:', fnew.exists(), ':', fnew)
        return

    fold_content = open(fold, encoding='utf-8').readlines()
    fnew_content = open(fnew, encoding='utf-8').readlines()

    # diff = difflib.HtmlDiff().make_file(fold_content, fnew_content, fold.name, fnew.name)
    # fhtml = Path(fnew.parent, 'diff_'+fold.stem+'.html')
    # with open(fhtml, 'w', encoding='utf-8') as f:
    #     f.write(diff)
    # print(fhtml)

    fdiff = Path(fnew.parent, 'diff_'+fold.stem+'.diff')
    with open(fdiff, 'w', encoding='utf-8') as f:
        diff = difflib.unified_diff(fold_content, fnew_content, fold.name, fnew.name)
        # sys.stdout.writelines(diff)
        f.writelines(diff)
    print(fdiff)

###########################################
def main(fold, fnew):
    fold = Path(fold)
    fnew = Path(fnew)

    if not fold.exists() or not fnew.exists():
        print('NOT' if not fold.exists() else ' '*3, 'exists:', fold)
        print('NOT' if not fnew.exists() else ' '*3, 'exists:', fnew)
        return

    if fold.is_dir() and fnew.is_dir():
        dir_compare(fold, fnew)
    elif fold.is_file() and fnew.is_file():
        file_compare(fold, fnew)

###########################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fnew')
    parser.add_argument('fold')
    args = parser.parse_args()
    main(args.fold, args.fnew)
