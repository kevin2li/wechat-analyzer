export_dir="/storage/emulated/0/Pictures/export"  # 媒体数据导出存储目录
base_dir="/data/data/com.tencent.mm/MicroMsg"
media_dir="/sdcard/Android/data/com.tencent.mm/MicroMsg"

base_id=$(basename "$( find $base_dir -name 'EnMicroMsg.db' -exec dirname {} \; )")
media_id=$(cat "$base_dir/$base_id/account.mapping")

echo "get base_id: $base_id"
echo "get media_id: $media_id"

if [ -d $export_dir ]; then
  echo "export dir: $export_dir already exists, please specify another one!"
  exit 1
else
  mkdir -p ${export_dir}
fi

cp "$base_dir/$base_id/EnMicroMsg.db" ${export_dir}
cp "$base_dir/$base_id/WxFileIndex.db" ${export_dir}
cp "/data/data/com.tencent.mm/shared_prefs/auth_info_key_prefs.xml" ${export_dir}

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
path="${media_dir}//Download"
echo "[5/5] copy Download directory..."
if [ -d $path ]; then
  cp -r $path $export_dir
else
  echo "${path} does not exists!"
fi

echo "Done!"
