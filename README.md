# 微信聊天记录分析器
> 注意：本教程主要关注Android设备，IOS设备可参考其他仓库，如[WechatExporter](https://github.com/BlueMatthew/WechatExporter)等

## 流程分析
### 1. 数据获取  

思路：由于Android手机没有root权限，先将聊天记录迁移到安卓模拟器，打开模拟器的root权限，然后从中提取以下两个文件:
- `/data/data/com.tencent.mm/MicroMsg/[32位随机字符]/EnMicroMsg.db`  
该文件是聊天记录存储数据库，类型为加密后的sqlite数据库。(注意：32位随机字符目录应该有两个，含有`EnMicroMsg.db`的目录才是我们要用的)。

- `/data/data/com.tencent.mm/shared_prefs/auth_info_key_prefs.xml`  
该文件包含`uin`值，下面破解密码会用到。

### 2. 数据库解密  

密码： `MD5(IMEI+uin)[:7]`

其中：
- `IMEI`: 一般取`1234567890ABCDEF`
- `uin`: 可从`/data/data/com.tencent.mm/shared_prefs/auth_info_key_prefs.xml`获取

![](https://minio.kevin2li.top/image-bed/202305150914913.png)

红框标注的即为`uin`。

运行下面的命令，输出最终的密码
```bash
./md5sum 1234567890ABCDEF {uin} # 输出："password: xxxxxxx"
```

### 3. 数据库查看

推荐使用[SqliteStudio](https://github.com/pawelsalawa/sqlitestudio/releases)查看加密后的数据库。

注意打开时添加如下加密算法配置选项：
```ini
PRAGMA cipher_use_hmac = OFF;
PRAGMA kdf_iter = 4000;
PRAGMA cipher_page_size = 1024;
PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1;
PRAGMA cipher_hmac_algorithm = HMAC_SHA1;
```

连接参数配置示例如下：

![](https://minio.kevin2li.top/image-bed/202305150926241.png)

打开成功示例：

![](https://minio.kevin2li.top/image-bed/202305150927750.png)
### 4. 数据库分析
xx

## 使用

xx