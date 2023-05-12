#!/usr/bin/env python3
# taken from https://github.com/anibali/h36m-fetch
from os import path, makedirs
import tarfile
from tqdm import tqdm
import argparse


subjects = ['S1', 'S5', 'S6', 'S7', 'S8', 'S9', 'S11']


# https://stackoverflow.com/a/6718435
def commonprefix(m):
    s1 = min(m)
    s2 = max(m)
    return next((s1[:i] for i, c in enumerate(s1) if c != s2[i]), s1)


def extract_tgz(tgz_file, dest):
    if path.exists(dest):
        return
    with tarfile.open(tgz_file, 'r:gz') as tar:
        members = [m for m in tar.getmembers() if m.isreg()]
        member_dirs = [path.dirname(m.name).split(path.sep) for m in members]
        base_path = path.sep.join(commonprefix(member_dirs))
        for m in members:
            m.name = path.relpath(m.name, base_path)
        tar.extractall(dest)


def extract_all():
    for subject_id in tqdm(subjects, ascii=True):
        out_dir = path.join('extracted', subject_id)
        makedirs(out_dir, exist_ok=True)
        (
            extract_tgz(
                f'archives/Poses_D3_Positions_mono_universal_{subject_id}.tgz',
                path.join(out_dir, 'Poses_D3_Positions_mono_universal'),
            ),
        )
        extract_tgz(f'archives/Videos_{subject_id}.tgz', path.join(out_dir, 'Videos'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datadir", type=str,
                        help="path to the data", required=True)
    args = parser.parse_args()
    ddir = args.datadir
    extract_all()
