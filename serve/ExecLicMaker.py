import shutil
import subprocess
from pathlib import Path
from config import *


def lic_maker_singel(mac: str):
    # mac:  00:1f:c1:00:00:00
    cmd = ['sudo', './lic_maker', 'single', mac]
    try:
        print(os.getcwd())
        p = subprocess.run(cmd, cwd=root_dir, timeout=10)
        return True
    except Exception as err:
        print(err)
        return False


def exec_lic_maker_singel(mac):
    # mac:  00:1f:c1:00:00:00
    old_name = 'lic_' + mac.replace(':', '') + '_en'
    new_name = 'lic_' + mac.replace(':', '') + '.lic'
    old_path = os.path.join(temp_dir, old_name)
    new_path = os.path.join(temp_dir, new_name)
    if Path(old_path).exists():
        os.remove(old_path)
    if Path(new_path).exists():
        os.remove(new_path)
    if lic_maker_singel(mac):
        os.rename(old_path, new_path)
        return True
    else:
        return False


def zip_file(zip_name):
    """
    zip all file in licen_output
    """
    import zipfile
    import os
    zip_name = '%s.zip' % zip_name
    zip_path = os.path.join(out_dir, zip_name)
    try:
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_LZMA) as f:
            for file in os.listdir(temp_dir):
                f.write(os.path.join(temp_dir, file), file)
            f.close()
        return True
    except Exception:
        return False
