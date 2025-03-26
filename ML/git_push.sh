#!/bin/bash

# Git 自动推送脚本
# 功能：依次执行 git add -> git commit -> git push
# 用法：1. 给脚本执行权限 chmod +x gitpush.sh 
#      2. 运行脚本 ./gitpush.sh "你的提交信息"

# 检查是否在Git仓库中
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "错误：当前目录不是Git仓库！"
    exit 1
fi

# 检查是否有未提交的更改
if [ -z "$(git status --porcelain)" ]; then
    echo "没有检测到文件变更，无需提交。"
    exit 0
fi

# 获取提交信息（支持命令行参数或交互式输入）
if [ -n "$1" ]; then
    commit_msg="$1"
else
    read -p "请输入提交信息: " commit_msg
    if [ -z "$commit_msg" ]; then
        echo "错误：提交信息不能为空！"
        exit 1
    fi
fi

# 执行Git操作
echo "正在执行 git add ..."
git add . || {
    echo "错误：git add 失败！"
    exit 1
}

echo "正在执行 git commit ..."
git commit -m "$commit_msg" || {
    echo "错误：git commit 失败！"
    exit 1
}

echo "正在执行 git push ..."
git push || {
    echo "错误：git push 失败！"
    exit 1
}

echo "✅ 所有操作已完成！"
