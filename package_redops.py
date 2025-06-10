from pathlib import Path
import shutil

project_root = Path(__file__).resolve().parents[0]

source_dir = project_root / "RedOps"
deb_target_dir = project_root / "builds" / "deb" / "opt" / "redops"
exe_target_dir = project_root / "builds" / "exe" / "RedOps"

def copy_tree(src, dst):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

copy_tree(source_dir, deb_target_dir)
copy_tree(source_dir, exe_target_dir)

