#!/usr/bin/env python3
"""
Script to download and extract the full UCF101 dataset and its official train/test splits
using wget (with --no-check-certificate), unrar, and unzip (no additional Python archive libraries required).
"""
import os
import argparse


def download_file(url, dst_dir):
    """
    Download a file via wget with support for resumable downloads and skipping certificate checks.
    Returns the local file path.
    """
    os.makedirs(dst_dir, exist_ok=True)
    local_path = os.path.join(dst_dir, os.path.basename(url))
    # --no-check-certificate to bypass SSL certificate verification
    cmd = f"wget --no-check-certificate -c -P {dst_dir} {url}"
    print(f"Downloading {url} to {dst_dir}...")
    os.system(cmd)
    return local_path


def extract_rar(rar_path, dst_dir):
    """
    Extract a .rar archive using the system's unrar utility.
    """
    os.makedirs(dst_dir, exist_ok=True)
    cmd = f"unrar x -idq {rar_path} {dst_dir}"
    print(f"Extracting {rar_path} to {dst_dir}...")
    os.system(cmd)


def extract_zip(zip_path, dst_dir):
    """
    Extract a .zip archive using the system's unzip utility.
    """
    os.makedirs(dst_dir, exist_ok=True)
    cmd = f"unzip -q {zip_path} -d {dst_dir}"
    print(f"Extracting {zip_path} to {dst_dir}...")
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser(
        description="Download and extract UCF101 dataset and its train/test splits."
    )
    parser.add_argument(
        '--download-dir', 
        type=str, 
        default='UCF101',
        help='Directory to download and extract the dataset.'
    )
    args = parser.parse_args()
    base_dir = args.download_dir

    # URLs for dataset and splits
    urls = {
        'UCF101.rar': 'https://www.crcv.ucf.edu/data/UCF101/UCF101.rar',
        'RecognitionSplits.zip': 'https://www.crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-RecognitionTask.zip',
        # 'DetectionSplits.zip': 'https://www.crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-DetectionTask.zip'
    }

    # Download and extract each
    for name, url in urls.items():
        local_path = download_file(url, base_dir)
        # only extract if download succeeded
        if os.path.exists(local_path):
            if local_path.endswith('.rar'):
                extract_rar(local_path, base_dir)
            elif local_path.endswith('.zip'):
                extract_zip(local_path, base_dir)
        else:
            print(f"Warning: {local_path} not found, skipping extraction.")

    print(f"\nAll available files downloaded and extracted to '{base_dir}'.")

if __name__ == '__main__':
    main()
