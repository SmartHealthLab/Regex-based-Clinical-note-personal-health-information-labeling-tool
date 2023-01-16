# python label.py smc 2>&1 | tee -a logs/label.smc.log

import argparse
from functools import partial
import sys
from elapsed import Elapsed
import yaml
from pathlib import Path
import regex as rx
import pandas as pd
from tqdm import tqdm
import multiprocessing as mp
import numpy as np
import platform

###########################################
def load_config(configs):
    yml = ''
    for config in configs:
        with open(config, encoding='utf-8') as f:
            yml += f.read() + '\n'
    return yaml.load(yml, Loader=yaml.FullLoader)

###########################################
def find_pattern(pts, k, name='exception'):
    x = [p[k][name] for p in pts if k in p and name in p[k]]
    return x[0] if len(x) > 0 else None

###########################################
def add_label(row, colname, pattern, pts, company, formaton, flog):
    def _rep(x):
        # print(x)
        k, v = [(k, v) for k, v in x.groupdict().items() if v != None and not k.startswith('__')][0]

        ex = find_pattern(pts, k, 'exception')
        if ex is not None and rx.search(ex, v) is not None:
            return v

        it, nm = k.split('__', 1)
        if flog is not None:
            flog.write(f'\n{row.name+1}: {it}.{nm}: {v}')

        format_str = f' format="{nm}"' if formaton else ''
        if company == 'SMC':
            return f'<{it}{format_str}>{v}</{it}>'
        return f'<deid item="{it}"{format_str}>{v}</deid>'

    replaced = pattern.sub(_rep, row[0])
    if replaced != row[0]:
        flog.write('\n')

    if flog is not None:
        org = row[0].split('\n')
        new = replaced.split('\n')
        for ii, line in enumerate(org):
            if line != new[ii]:
                # flog.write(f'\torg: {line}\n')
                flog.write(f'\t[{ii+1}]: {new[ii]}')
    # if (row.name+1) % 1000 == 0:
    #     print(f'{colname}: row: {row.name+1}')
    return replaced

###########################################
def make_alias(cfg):
    pattern = rx.compile(r'\$\{[_\w]+\}')

    def _rxp(x):
        k = x.group()[2:-1]
        if k not in cfg['alias']:
            raise KeyError(f'No alias: {k}')

        v = cfg['alias'][k]
        m = pattern.search(v)
        return v if m == None else pattern.sub(_rxp, v)

    for k, v in cfg['alias'].items():
        cfg['alias'][k] = pattern.sub(_rxp, v)
    return cfg

###########################################
def get_patterns(cfg):
    _rxp = lambda x: cfg['alias'][x.group()[2:-1]]

    pattern = rx.compile(r'\$\{[_\w]+\}')

    rep = []
    for item in cfg['items']:
        it, fms = list(item.items())[0]
        for fm in fms:
            k, v = list(fm.items())[0]
            tmp = {}
            for x in ['pattern', 'exception']:
                if x not in v:
                    continue
                tmp[x] = pattern.sub(_rxp, v[x])
            rep.append({f'{it}__{k}': tmp})
    return rep

###########################################
def make_pattern(rep):
    pts = []
    for item in rep:
        k, v = list(item.items())[0]
        pts.append(f'(?P<{k}>{v["pattern"]})')
    return '|'.join(pts)

###########################################
def test_patterns(rep):
    ret = True
    for item in rep:
        k, v = list(item.items())[0]
        for x in ['pattern', 'exception']:
            if x not in v:
                continue
            try:
                # print(f'{k}: {v[x]}')
                # pattern = rx.compile(f'(?P<{k}>{v[x]})', flags=rx.I|rx.MULTILINE)
                pattern = rx.compile(f'(?P<{k}>{v[x]})', flags=rx.I)
            except rx.error as e:
                print(f'[E] {k}\n\t{x}: {v[x]}\n\t{e}')
                ret = False
                return False
    return ret
    
###########################################
def labeling_tqdm(args, df):
    # 잔상이 남아서 보기 더 안 좋네
    # tqdm.pandas(position=int(mp.current_process()._identity[0]))
    tqdm.pandas()
    df[args[0]] = df[args[0]].to_frame().progress_apply(add_label, axis=1, args=args)
    return df

# ###########################################
# def labeling(args, df):
#     df[args[0]] = df[args[0]].to_frame().apply(add_label, axis=1, args=args)
#     return df

###########################################
def parallel_df(df, fn, args):
    cpu_cnt = mp.cpu_count()
    df_split = np.array_split(df, cpu_cnt)
    pool = mp.Pool(cpu_cnt)
    fnp = partial(fn, args)
    df = pd.concat(pool.map(fnp, df_split))
    pool.close()
    pool.join()
    return df

###########################################
def main(configs, findlog):
    elapsed = Elapsed()
    # print('config:', config)
    
    cfg = load_config(configs)
    company = cfg['company'] if 'company' in cfg else None
    formaton = cfg['format'] if 'format' in cfg else False

    path = Path(cfg['data']['root'], cfg['data']['in']).absolute()

    cfg = make_alias(cfg)
    pts = get_patterns(cfg)

    if not test_patterns(pts):
        sys.exit(9)

    pattern_str = make_pattern(pts)
    # print(pattern_str)
    
    # pattern = rx.compile(pattern_str, flags=rx.I|rx.MULTILINE)
    pattern = rx.compile(pattern_str, flags=rx.I)

    flog_root = Path(cfg['data']['root'], '_findlog')
    flog_root.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(path, header=cfg['data']['header'], dtype=object, na_filter=False)
    # print(df.info)
    # for c in cfg['columns']:
    for c in df.columns:
        print('column:', c)
        f = None if not findlog else open(Path(flog_root, c+'.log'), 'w', encoding='utf-8')
        
        if platform.system() == 'Windows':
            df = labeling_tqdm(df=df, args=(c, pattern, pts, company, formaton, f,))
        else:
            df = parallel_df(df, labeling_tqdm, args=(c, pattern, pts, company, formaton, f,))

        if f is not None:
            f.close()
            print('\tlog:', f.name)


    df.to_csv(Path(path.parent, cfg['data']['out']), header=True)
    print('\t', Path(path.parent, cfg['data']['out']))

    elapsed.print_elapsed()

###########################################
if __name__ == "__main__":
    _str2bool = lambda x: x.lower() in ['true', 'yes', 'y']
    
    parser = argparse.ArgumentParser()
    parser.add_argument('configs', nargs='+')
    parser.add_argument('-log', '--findlog', default=False, type=_str2bool)
    args = parser.parse_args()
    main(args.configs, args.findlog)
    