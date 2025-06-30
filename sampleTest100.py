#!/usr/bin/env python3
import os
import shutil
import argparse

def copy_files_with_structure(source_dir, file_list_path, target_dir):
    """
    Copy files listed in `file_list_path` from `source_dir` to `target_dir`, preserving directory structure.
    """
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Read file list
    with open(file_list_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        rel_path = line.strip()
        if not rel_path:
            continue

        src_file = os.path.join(source_dir, rel_path)
        if os.path.exists(src_file):
            dst_file = os.path.join(target_dir, rel_path)
            dst_dir = os.path.dirname(dst_file)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            shutil.copy2(src_file, dst_file)
            print(f"Copied: {src_file} -> {dst_file}")
        else:
            print(f"文件不存在: {src_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Copy files preserving directory structure."
    )
    parser.add_argument(
        "--source-dir", default="datasets/UCF101/test",
        help="Source directory path "
    )
    parser.add_argument(
        "--file-list", default="datasets/UCF101/TestList100.txt",
        help="Path to the file list txt "
    )
    parser.add_argument(
        "--target-dir", default="datasets/UCF101/test-101",
        help="Target directory path "
    )
    args = parser.parse_args()

    copy_files_with_structure(
        args.source_dir,
        args.file_list,
        args.target_dir
    )

if __name__ == "__main__":
    main()
