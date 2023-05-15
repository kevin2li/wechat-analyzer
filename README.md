# 微信聊天记录分析器
> 注意：本教程主要关注Android设备，IOS设备可参考其他仓库，如[WechatExporter](https://github.com/BlueMatthew/WechatExporter)等

## 流程分析

### 1. 数据获取  

思路：由于Android手机没有root权限，先将聊天记录迁移到安卓模拟器，打开模拟器的root权限，然后从中提取以下文件或目录:

- `/data/data/com.tencent.mm/MicroMsg/[32位随机字符]/EnMicroMsg.db`  
该文件是聊天记录存储数据库，类型为加密后的sqlite数据库。(注意：32位随机字符目录应该有两个，含有`EnMicroMsg.db`的目录才是我们要用的)。

- `/data/data/com.tencent.mm/MicroMsg/[32位随机字符]/WxFileIndex.db`  
该文件记录了文件索引，可以查找此表找到媒体文件(音频、视频、下载文件等)的实际存储位置。

- `/data/data/com.tencent.mm/shared_prefs/auth_info_key_prefs.xml`  
该文件包含`uin`值，下面破解密码会用到。

- `/data/data/com.tencent.mm/MicroMsg/[32位随机字符]/account.mapping`  
该文件包含一个32位随机字符串，是音频、视频等媒体文件在`/sdcard/Android/data/com.tencent.mm/MicroMsg`中的存储目录名称。


### 2. 数据库密码破解  

密码： `MD5(IMEI+uin)[:7]`

其中：
- `IMEI`: 一般取`1234567890ABCDEF`
- `uin`: 可从`/data/data/com.tencent.mm/shared_prefs/auth_info_key_prefs.xml`获取

![](https://minio.kevin2li.top/image-bed/202305150914913.png)

红框标注的即为`uin`。

运行下面的命令，输出最终的密码
```bash
./bin/md5sum 1234567890ABCDEF {uin} # 输出："password: xxxxxxx"
```

拿到密码后，可以发现`EnMicroMsg.db`和`WxFileIndex.db`这两个数据库文件都可以用这个密码打开。

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

![EnMicroMsg.db](https://minio.kevin2li.top/image-bed/202305150927750.png)

### 4. 数据库解密

前面通过破解的密码可以查看到数据库内容了，但是为了方便后面的分析，我们把它转成明文数据库。

```bash
# EnMicroMsg.db解密
docker run --rm -v C:\Users\kevin\Documents\leidian9\Pictures\export:/wcdb  greycodee/wcdb-sqlcipher -f EnMicroMsg.db -k abd1d68

# WxFileIndex.db解密
docker run --rm -v C:\Users\kevin\Documents\leidian9\Pictures\export:/wcdb  greycodee/wcdb-sqlcipher -f WxFileIndex.db -k abd1d68

```

### 4. 数据库分析
**表结构分析：**
#### 账号相关信息
- `userinfo`  

该表存放了本人账号相关的基本信息，包括微信id、昵称、手机号、邮箱、个性签名、地区等。

![](https://minio.kevin2li.top/image-bed/202305151300309.png)

- `rcontact`  

该表存放了该账号涉及的所有账号(包括微信好友、微信群等)的基本信息(eg：微信昵称，备注，原微信号，改之后的微信号，全拼等等)

![](https://minio.kevin2li.top/image-bed/202305151053063.png)

- `bizinfo`

该表存放的是该账号的好友微信号，群账号，这里好友包括已经通过的和添加没通过的。

![](https://minio.kevin2li.top/image-bed/202305151054930.png)

- `img_flag`

该表存放该账号所有涉及的微信(好友，同属一个群不是好友，添加的陌生人)的头像地址。

![](https://minio.kevin2li.top/image-bed/202305151054031.png)


#### 微信群
- `chatroom`  

该表存放了微信群相关的基本信息，包括群名称、群成员、群主等。

![](https://minio.kevin2li.top/image-bed/202305151058175.png)

#### 聊天记录信息
- `message`  

该表存放了跟聊天记录相关的信息，包括聊天内容、是否为发送方、创建时间等：  

![](https://minio.kevin2li.top/image-bed/202305151102942.png)

相关重要字段说明：

| 字段     | 说明                                                                          |
| -------- | ----------------------------------------------------------------------------- |
| msgSvrId | 唯一标识每条聊天记录的id                                                      |
| type     | 消息类型，详见下面的`聊天记录类型码说明`                                      |
| isSend   | 0: 接收 1：发送                                                               |
| talker   | 可以判断群消息还是个人消息，如果是群消息会有`@chatroom`结尾，否则为个人微信id |
| talkerId | xx                                                                            |
| content  | 聊天记录内容                                                                  |
| imgPath  | xx                                                                            |


聊天记录类型码说明：
| 消息类型码 | 说明                 |
| ---------- | -------------------- |
| 1          | 文本内容(包括小表情) |
| 3          | 图片                 |
| 34         | 语音                 |
| 43         | 视频                 |
| 47         | 大表情               |
| 49         | 文件                 |
| 10000      | 撤回消息提醒         |
| 436207665  | 微信红包             |
| 419430449  | 微信转账             |

**媒体文件实际存储位置：**
- 图片  

`/data/data/com.tencent.mm/MicroMsg/[32位字母]/image2`

- 头像

`/data/data/com.tencent.mm/MicroMsg/[32位字母]/avatar`


- 语音

`/sdcard/Android/data/com.tencent.mm/MicroMsg/[32位字母]/voice2`


- 视频

`/sdcard/Android/data/com.tencent.mm/MicroMsg/[32位字母]/video`

- 文件

`/sdcard/Android/data/com.tencent.mm/MicroMsg/Download`




## 使用

xx


## 参考资料

1. [InfoQ | 解密安卓微信聊天信息存储](https://xie.infoq.cn/article/ef3e8d9742658c455024a2614#:~:text=message%20%E7%9A%84%20imgPath%20%E5%AD%97%E6%AE%B5%E9%80%9A%E8%BF%87%20MD5,%E5%8A%A0%E5%AF%86%20%E5%90%8E%EF%BC%8C%E5%89%8D%204%20%E4%B8%AA%E5%AD%97%E6%AF%8D%E4%BB%A3%E8%A1%A8%E4%B8%A4%E7%BA%A7%E6%96%87%E4%BB%B6%E5%A4%B9%E5%90%8D%EF%BC%8C%E7%84%B6%E5%90%8E%E6%9C%80%E7%BB%88%E6%96%87%E4%BB%B6%E5%90%8D%E6%98%AF%EF%BC%9A%20msg_imgPath%E7%9A%84%E5%80%BC.amr)
2. [知乎 | 微信数据库解析总结](https://zhuanlan.zhihu.com/p/552876079?utm_campaign=shareopn&utm_medium=social&utm_oi=790165242284998656&utm_psn=1641221292434132992&utm_source=wechat_session)
3. 