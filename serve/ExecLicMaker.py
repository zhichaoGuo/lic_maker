import os
import subprocess
from pathlib import Path
from config import *
from serve.MacTool import is_mac, mac_17_2_12, gen_mac_list


def lic_maker_singel(mac: str):
    # mac:  00:1f:c1:00:00:00
    lic_maker_path = os.path.join(root_dir, 'lic_maker')
    cmd = ['sudo', lic_maker_path, 'single', mac]
    try:
        print(os.getcwd())
        p = subprocess.run(cmd, cwd=root_dir, timeout=10)
        # print(p.returncode)
        if p.returncode == 0:
            return True
        return False
    except Exception as err:
        print(err)
        return False


def lic_maker_range(start_mac: str, stop_mac: str):
    # mac:  00:1f:c1:00:00:00
    lic_maker_path = os.path.join(root_dir, 'lic_maker')
    cmd = ['sudo', lic_maker_path, 'range', start_mac, stop_mac]
    try:
        print(os.getcwd())
        p = subprocess.run(cmd, cwd=root_dir, timeout=10)
        # print(p.returncode)
        if p.returncode != -1:
            return True
        return False
    except Exception as err:
        print(err)
        return False


def exec_lic_maker_singel(mac):
    """ 传进 00:1F:C1:00:00:10，生成文件后 会改名"""
    # if is_mac(mac):
    #     old_name = 'lic_' + mac.replace(':', '') + '_en'
    #     new_name = 'lic_' + mac.replace(':', '') + '.lic'
    #     old_path = os.path.join(temp_dir, old_name)
    #     new_path = os.path.join(temp_dir, new_name)
    #     if Path(old_path).exists():
    #         os.remove(old_path)
    #     if Path(new_path).exists():
    #         os.remove(new_path)
    #     if lic_maker_singel(mac):
    #         p = subprocess.run(['sudo', 'chmod', '777', old_name], cwd=temp_dir, timeout=10)
    #         if p.returncode == 0:
    #             os.rename(old_path, new_path)
    #             return True
    #         else:
    #             os.remove(old_path)
    #     return False
    # else:
    #     return False
    return lic_maker_singel(mac)


def exec_lic_maker_range(start_mac:str,stop_mac:str):
    """ 传进 00:1F:C1:00:00:10，生成文件后 会改名"""
    # all_mac_list = gen_mac_list(start_mac,stop_mac)
    # for mac in all_mac_list:
    #     old_name = 'test' + mac.replace(':', '') + '_en.lic'
    #     new_name = 'lic_' + mac.replace(':', '') + '.lic'
    #     old_path = os.path.join(temp_dir, old_name)
    #     new_path = os.path.join(temp_dir, new_name)
    #     if Path(old_path).exists():
    #         os.remove(old_path)
    #     if Path(new_path).exists():
    #         os.remove(new_path)
    # lic_maker_range(start_mac,stop_mac)
    # for mac in all_mac_list:
    #     old_name = 'test' + mac.replace(':', '') + '_en.lic'
    #     new_name = 'lic_' + mac.replace(':', '') + '.lic'
    #     old_path = os.path.join(temp_dir, old_name)
    #     new_path = os.path.join(temp_dir, new_name)
    #     os.rename(old_path,new_path)
    return lic_maker_range(start_mac,stop_mac)


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
                p = subprocess.run(['sudo', 'chmod', '777', file], cwd=temp_dir, timeout=10)
                f.write(os.path.join(temp_dir, file), file)
            f.close()
        return True
    except Exception:
        return False


def clean_temp_dir():
    if Path(temp_dir).exists():
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
    else:
        Path(temp_dir).mkdir()
