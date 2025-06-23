#!/usr/bin/env python3
"""
Script to split UCF-101 videos into train/test directories at the same level as the original folder,
then recursively remove any empty subdirectories under 'UCF-101' and finally delete 'UCF-101'.
"""
import os
import os.path as osp
import shutil
import argparse


def move_files(root, filenames, split):
    """
    Move a list of video filenames into a split directory under root.

    Args:
        root (str): Base directory containing 'UCF-101' and 'ucfTrainTestlist'.
        filenames (list[str]): Relative paths of videos to move.
        split (str): Subdirectory name, e.g., 'train' or 'test'.
    """
    dest_split = osp.join(root, split)
    os.makedirs(dest_split, exist_ok=True)
    for rel_path in filenames:
        src = osp.join(root, 'UCF-101', rel_path)
        dst = osp.join(dest_split, rel_path)
        os.makedirs(osp.dirname(dst), exist_ok=True)
        shutil.move(src, dst)


def parse_list(path, is_train=True):
    """
    Parse a trainlist or testlist file.

    Args:
        path (str): Path to the list file.
        is_train (bool): Whether this is a train list (includes labels).

    Returns:
        list[str]: List of relative file paths.
    """
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    if is_train:
        return [line.split()[0] for line in lines]
    return lines


def remove_empty_dirs(path):
    """
    Recursively remove empty directories under given path.
    """
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        # If no files and no subdirectories, remove
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
                print(f"Removed empty directory '{dirpath}'.")
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(
        description="Split UCF-101 into train/test at root level and remove empty source folder."
    )
    parser.add_argument(
        '--root', '-r',
        type=str,
        default='.',
        help="Base directory containing 'UCF-101' and 'ucfTrainTestlist'."
    )
    parser.add_argument(
        '--fold', '-f',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Fold index to use (1, 2, or 3)."
    )
    args = parser.parse_args()

    ucf_dir = osp.join(args.root, 'UCF-101')
    list_dir = osp.join(args.root, 'ucfTrainTestlist')
    train_list = osp.join(list_dir, f'trainlist0{args.fold}.txt')
    test_list = osp.join(list_dir, f'testlist0{args.fold}.txt')

    # Validate directories
    if not osp.isdir(ucf_dir):
        raise FileNotFoundError(f"Could not find UCF-101 directory under {args.root}")
    if not osp.isdir(list_dir):
        raise FileNotFoundError(f"Could not find ucfTrainTestlist under {args.root}")

    # Parse and move train files
    train_files = parse_list(train_list, is_train=True)
    move_files(args.root, train_files, 'train')

    # Parse and move test files
    test_files = parse_list(test_list, is_train=False)
    move_files(args.root, test_files, 'test')

    # Recursively remove empty subdirectories
    remove_empty_dirs(ucf_dir)
    # Finally remove the top-level UCF-101 if it's empty
    try:
        os.rmdir(ucf_dir)
        print(f"Removed directory '{ucf_dir}'.")
    except OSError:
        print(f"Warning: '{ucf_dir}' not empty or could not be removed.")

    print(f"Moved {len(train_files)} train files and {len(test_files)} test files for fold {args.fold}.")

if __name__ == '__main__':
    main()
