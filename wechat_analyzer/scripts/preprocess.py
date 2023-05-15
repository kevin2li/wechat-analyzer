import hashlib
import os
import re
import sys
from pathlib import Path
from loguru import logger

base_dir = "C:/Users/kevin/Documents/leidian9/Pictures/export"

def extract_uin(path: str = "system_config_prefs.xml"):
    with open(path, "r", encoding='utf-8') as f:
        for line in f:
            if "uin" in line:
                m = re.search("(?<=value=\")(.+)(?=\")", line)
                if m is not None:
                    return m.group(1)
    return None


def gen_password(IMEI: str, uin: str, output_path: str = None):
    s = IMEI + uin
    hash_object = hashlib.md5(s.encode())
    hash_str = hash_object.hexdigest()
    password = hash_str[:7]
    logger.success(f"获取密码成功: {password}")
    if output_path is None:
        with open(os.path.join(base_dir, "password.txt"), 'w', encoding="utf-8") as f:
            f.write(password)
    return password

def convert_audio(audio_dir: str):
    cmd = f"docker run --rm -v {audio_dir}:/media  greycodee/silkv3-decoder"
    os.system(cmd)


def decrypt_db(path: str, key: str):
    p = Path(path)
    cmd = f"docker run --rm -v {p.parent}:/wcdb  greycodee/wcdb-sqlcipher -f {p.name} -k {key}"
    os.system(cmd)


def main():
    # 破解密码
    logger.info("[1/3] 破解密码...")
    uin_path = str(Path(base_dir) / "auth_info_key_prefs.xml")
    uin = extract_uin(uin_path)
    if uin:
        IMEI = "1234567890ABCDEF"
        key = gen_password(IMEI=IMEI, uin=uin)
    else:
        logger.error("尝试破解密码失败！")
        sys.exit(1)

    # 解密数据库
    logger.info("[2/3] 解密数据库...")
    logger.info("1) 解密EnMicroMsg.db")
    path1 = str(Path(base_dir) / "EnMicroMsg.db")
    decrypt_db(path1, key)

    logger.info("2) 解密WxFileIndex.db")
    path2 = str(Path(base_dir) / "WxFileIndex.db")
    decrypt_db(path2, key)

    # 转换音频
    logger.info("[3/3] 转换音频...")
    path3 = str(Path(base_dir) / "voice2")
    convert_audio(path3)

    logger.success("Done!")

if __name__ == "__main__":
    main()
