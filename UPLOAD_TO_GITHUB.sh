#!/bin/bash

# H200 Test System - GitHub Upload Script
# 使用说明: bash UPLOAD_TO_GITHUB.sh <github_username> <github_token>

if [ $# -lt 2 ]; then
    echo "使用方法: bash UPLOAD_TO_GITHUB.sh <github_username> <github_token_or_password>"
    echo ""
    echo "示例:"
    echo "  bash UPLOAD_TO_GITHUB.sh myusername ghp_xxxxxxxxxxxxxxxxxxxx"
    echo ""
    echo "或使用 SSH 密钥（如已配置）:"
    echo "  bash UPLOAD_TO_GITHUB.sh ssh"
    exit 1
fi

USERNAME=$1
TOKEN_OR_SSH=$2

echo "================================"
echo "H200 Test System - GitHub Upload"
echo "================================"
echo ""

# 检查 Git 状态
echo "检查 Git 状态..."
git status

echo ""
echo "当前提交:"
git log --oneline -n 1

echo ""
echo "准备上传到 GitHub..."
echo "用户名: $USERNAME"
echo ""

if [ "$TOKEN_OR_SSH" = "ssh" ]; then
    echo "使用 SSH 密钥上传..."
    REPO_URL="git@github.com:$USERNAME/H200_Test.git"
else
    echo "使用 HTTPS Token 上传..."
    REPO_URL="https://$USERNAME:$TOKEN_OR_SSH@github.com/$USERNAME/H200_Test.git"
fi

# 添加远程地址
echo ""
echo "添加远程地址..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

# 验证远程地址
echo "远程地址配置:"
git remote -v

# 推送到 GitHub
echo ""
echo "推送代码到 GitHub..."
git push -u origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 上传成功！"
    echo ""
    echo "仓库地址: https://github.com/$USERNAME/H200_Test"
    echo ""
    echo "后续步骤:"
    echo "  1. 添加 LICENSE 文件"
    echo "  2. 更新仓库描述和主页"
    echo "  3. 启用 GitHub Pages（可选）"
    echo "  4. 配置分支保护规则（可选）"
else
    echo ""
    echo "❌ 上传失败！"
    echo "请检查:"
    echo "  • GitHub 用户名是否正确"
    echo "  • Token 或 SSH 密钥是否有效"
    echo "  • H200_Test 仓库是否已在 GitHub 上创建"
    exit 1
fi
