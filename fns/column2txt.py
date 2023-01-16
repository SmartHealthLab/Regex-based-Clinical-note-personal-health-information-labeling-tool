# python column2txt.py 2>&1 | tee -a logs/column2txt.log

import argparse
import pandas as pd
from pathlib import Path
from elapsed import Elapsed
import math


def main(inpath, colname, cnt, outpath):
    elapsed = Elapsed()

    df = pd.read_csv(Path(inpath), header=0, dtype=object, na_filter=False)
    total_rows = len(df)
    if cnt == -1:
        cnt = total_rows

    Path(outpath).parent.mkdir(parents=True, exist_ok=True)

    if colname not in df.columns.values:
        print('NOT EXISTS: column:', colname)
        return

    # out_base = Path(outpath.replace('#','_'))
    out_base = Path(outpath)

    fnos = math.ceil(total_rows / cnt)
    for fno in range(1, fnos+1):
        out_file = Path(out_base.parent, out_base.stem + f'.{fno:02}{out_base.suffix}')
        with open(out_file, mode='w', encoding='utf-8') as f:
            endrow = total_rows if total_rows < fno * cnt else fno * cnt
            for ii in range((fno-1)*cnt, endrow):
                if not pd.isna(df.iloc[ii][colname]):
                    f.write('-------------------------------\n')
                    f.write(f'\t{ii+1}\n')
                    f.write('-------------------------------\n')
                    f.write(f'{df.iloc[ii][colname]}\n')
                    # if (ii+1) % 1000 == 0:
                    #     print(out_file.name, 'row:', ii+1, flush=True)
        print(out_file.name, 'row:', (fno-1)*cnt+1, '-', ii+1, flush=True)
        # f.close()
    elapsed.print_elapsed()

###########################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inpath')
    parser.add_argument('-c', '--column')
    parser.add_argument('-n', '--count', type=int, default=-1)
    parser.add_argument('-o', '--outpath')
    args = parser.parse_args()
    main(args.inpath, args.column, args.count, args.outpath)
