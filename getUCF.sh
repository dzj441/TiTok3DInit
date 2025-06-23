download_dir="/path/to/ucf_data"  # 修改为你的目标路径
fold=1                             # 选择折数（1、2 或 3）

# 两行调用：先下载解压，再拆分目录
python3 download_ucf101.py --download-dir "$download_dir"
python3 move_ucf_splits.py --root "$download_dir" --fold "$fold"
