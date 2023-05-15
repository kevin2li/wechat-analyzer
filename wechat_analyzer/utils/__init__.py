import os
from pathlib import Path


def parse_img_path(img_path: str, base_dir: str, is_send: int, wxid: str, talker: str, msgSrvid: str):
    """_summary_
    img_path examples:
    1. THUMBNAIL_DIRPATH://th_e41d5c85c815d5cbc553c2578d58c9ef
    2. 7baf454e59c41b60746fe7740c5e54b6

    Args:
        img_path (str): message表中图片路径
    """
    if img_path.startswith("THUMB"):
        realpath = str(Path(base_dir) / img_path[23:25] / img_path[25:27] / img_path[20:])
        return realpath
    else:
        if is_send: # 发送
            filename = "_".join([wxid, talker, msgSrvid, '_backup'])
            realpath = str(Path(base_dir) / filename[:2] / filename[2:4] / filename)
        else: # 接收
            filename = "_".join([talker, wxid, msgSrvid, '_backup'])
            realpath = str(Path(base_dir) / filename[:2] / filename[2:4] / filename)
    return realpath


def parse_file_path(img_path):
    pass


if __name__ == '__main__':
    base_dir = "C:/Users/kevin/Documents/leidian9/Pictures/export/image2"
    # img_path = "7baf454e59c41b60746fe7740c5e54b6"
    img_path = "THUMBNAIL_DIRPATH://th_e41d5c85c815d5cbc553c2578d58c9ef"
    talker = "39152718862@chatroom"
    wxid = "wxid_o43ubt7awgxu22"
    msgSrvid = "5411526890239366823"
    is_send = 0
    out = parse_img_path(img_path, base_dir, is_send, wxid, talker, msgSrvid)
    print(out)