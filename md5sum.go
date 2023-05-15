package main

import (
    "crypto/md5"
    "encoding/hex"
    "fmt"
    "os"
)

func main() {
    // 获取命令行参数
    args := os.Args[1:]

    // 如果没有提供两个参数，输出帮助信息
    if len(args) != 2 {
        fmt.Println("Usage: md5sum IMEI uin")
        return
    }

    // 拼接字符串
    str := args[0] + args[1]

    // 计算 MD5 值
    md5Hash := md5.Sum([]byte(str))

    // 将 MD5 值转为十六进制字符串
    md5Str := hex.EncodeToString(md5Hash[:])
	fmt.Printf("password: %s\n", md5Str[:7])
}
