base_id="8fd34265d5703d242da91e26614da411"        # 32位随机字符1((位于/data/data/com.tencent.mm/MicroMsg下))
media_id="7efeaab26d8444e38fb01b09d5bb71bf"       # 32位随机字符2(位于/sdcard/Android/data/com.tencent.mm/MicroMsg下)
export_dir="/storage/emulated/0/Pictures/export"  # 媒体数据导出存储目录


base_dir="/data/data/com.tencent.mm/MicroMsg"
media_dir="/sdcard/Android/data/com.tencent.mm/MicroMsg"

mkdir -p ${export_dir}

# 拷贝图片
echo "[1/5] copy image2 directory..."
path="${base_dir}/${base_id}/image2"
if [ -d $path ]; then
  cp -r $path $export_dir
else
  echo "${path} does not exists!"
fi

# 拷贝头像
echo "[2/5] copy avatar directory..."
path="${base_dir}/${base_id}/avatar"
if [ -d $path ]; then
  cp -r $path $export_dir
else
  echo "${path} does not exists!"
fi

# 拷贝音频
echo "[3/5] copy voice2 directory..."
path="${media_dir}/${media_id}/voice2"
if [ -d $path ]; then
  cp -r $path $export_dir
else
  echo "${path} does not exists!"
fi

# 拷贝视频
path="${media_dir}/${media_id}/video"
echo "[4/5] copy video directory..."
if [ -d $path ]; then
  cp -r $path $export_dir
else
  echo "${path} does not exists!"
fi

# 拷贝下载文件
path="${media_dir}/${media_id}/Download"
echo "[5/5] copy Download directory..."
if [ -d $path ]; then
  cp -r $path $export_dir
else
  echo "${path} does not exists!"
fi
