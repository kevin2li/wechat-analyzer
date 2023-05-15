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
    
    // 如果没有提供参数，输出帮助信息
	if len(args) == 0 {
		fmt.Println("Please provide one or more strings to calculate MD5")
		return
	}

    // 拼接字符串
    str := ""
	for _, arg := range args {
        str += arg
	}

    // 计算 MD5 值
    md5Hash := md5.Sum([]byte(str))
    
    // 将 MD5 值转为十六进制字符串
    md5Str := hex.EncodeToString(md5Hash[:])
    fmt.Printf("MD5: %s\n", md5Str)
    fmt.Printf("password: %s\n", md5Str[:7])
}
