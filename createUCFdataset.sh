#!/usr/bin/env bash


# Base directories (modify as needed)
dataset_dir="/root/autodl-tmp"    # 数据集根目录
code_dir="/root/projects"         # 代码根目录

# Derived paths
download_dir="$dataset_dir/UCF101"   # 数据集完整路径
working_dir="$code_dir/TiTok3D"        # 代码项目路径
fold=1                                   # 选择划分方案（1、2 或 3）

# Ensure directories exist
mkdir -p "$download_dir"

# Download and extract dataset
python3 getUCF.py --download-dir "$download_dir"

# Split into train/test
target_dir="$download_dir"
python3 splitUCF.py --root "$target_dir" --fold "$fold"

# Create symlink in working_dir (link name: datasets)
ln -sfn "$dataset_dir" "$working_dir/datasets"

echo "download Pipeline complete."
echo "Dataset at: $download_dir"
echo "Symlink at: $working_dir/datasets"
echo "Train/Test split for fold $fold created under $download_dir"

python3 sampleTest100.py --source-dir "$download_dir/test" --file-list "TestList100.txt" --target-dir "$download_dir/test100"

mv testlist01.txt "$download_dir/"

mv trainlist01.txt "$download_dir/"

mv TestList100.txt "$download_dir/"
