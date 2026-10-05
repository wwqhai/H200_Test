# GitHub 上传完整指南

## 前置要求

### 1. GitHub 账户
- 已创建 GitHub 账户
- 已登录

### 2. 创建新仓库
访问 https://github.com/new 创建新仓库：
- **Repository name**: `H200_Test`
- **Description**: `H200 AI Cluster Testing and Validation System`
- **Visibility**: Public（或 Private）
- **Initialize with**: 不勾选任何选项（因为我们已有代码）

### 3. 获取凭证

#### 方式 A：使用 Personal Access Token（推荐）
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择 "Generate new token (classic)"
4. 设置：
   - Token name: `H200_Test_Upload`
   - Expiration: 自选（建议 90 days）
   - Scopes: 勾选 `repo` 和 `workflow`
5. 点击 "Generate token"
6. **复制 token**（只显示一次）

#### 方式 B：使用 SSH 密钥
如果已配置 SSH 密钥，可跳过 Token 方式。

## 上传步骤

### 方式 1：使用脚本（推荐）

```bash
cd h200-test-system

# 使用 Token 上传
bash UPLOAD_TO_GITHUB.sh YOUR_GITHUB_USERNAME YOUR_PERSONAL_ACCESS_TOKEN

# 或使用 SSH 密钥上传
bash UPLOAD_TO_GITHUB.sh YOUR_GITHUB_USERNAME ssh
```

### 方式 2：手动上传（HTTPS）

```bash
cd h200-test-system

# 配置凭证存储（Windows）
git config --global credential.helper manager-core

# 添加远程地址
git remote add origin https://github.com/YOUR_USERNAME/H200_Test.git

# 推送到 GitHub
git push -u origin master

# 输入用户名和 Token
# Username: YOUR_GITHUB_USERNAME
# Password: YOUR_PERSONAL_ACCESS_TOKEN
```

### 方式 3：手动上传（SSH）

```bash
cd h200-test-system

# 添加远程地址
git remote add origin git@github.com:YOUR_USERNAME/H200_Test.git

# 推送到 GitHub
git push -u origin master
```

## 上传成功验证

访问 `https://github.com/YOUR_USERNAME/H200_Test` 检查：

- [x] 所有文件已上传
- [x] README.md 显示正确
- [x] Git 提交历史显示
- [x] 代码文件完整

## 上传后操作

### 1. 添加 LICENSE

```bash
cd h200-test-system

# 创建 MIT License
cat > LICENSE << 'LICENCE_EOF'
MIT License

Copyright (c) 2026 H200 Test System Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
LICENCE_EOF

git add LICENSE
git commit -m "Add MIT LICENSE"
git push origin master
```

### 2. 更新仓库描述

在 GitHub 仓库页面右上角点击 Settings，更新：
- **Description**: H200 AI Cluster Testing and Validation System
- **Website**: （可选，添加项目文档链接）
- **Topics**: 添加 `h200`, `testing`, `validation`, `ai`, `gpu`

### 3. 启用 GitHub Pages（可选）

在 Settings > Pages 配置文档站点。

### 4. 配置分支保护规则（可选）

在 Settings > Branches 配置保护规则，防止直接推送到 master。

## 常见问题

### Q: 上传时出现 "fatal: not a git repository"
**A**: 确保在项目目录中：
```bash
cd h200-test-system
```

### Q: 显示 "Permission denied (publickey)"
**A**: SSH 密钥配置问题。使用 HTTPS 方式或重新配置 SSH 密钥。

### Q: 显示 "Authentication failed"
**A**: Token 或密码错误。检查：
- Token 未过期
- Token 有 `repo` 权限
- 用户名和 Token 正确

### Q: 如何撤销推送？
**A**: 不建议强制推送到公开仓库。建议：
```bash
git revert HEAD  # 创建反向提交
git push origin master
```

### Q: 如何更新已上传的代码？
**A**: 本地修改后正常推送：
```bash
cd h200-test-system
git add .
git commit -m "Your commit message"
git push origin master
```

## 后续开发工作流

### 创建特性分支
```bash
git checkout -b feature/your-feature-name
```

### 提交更改
```bash
git add .
git commit -m "Add your feature"
```

### 创建 Pull Request
```bash
git push origin feature/your-feature-name
# 然后在 GitHub 上创建 PR
```

### 合并到 master
在 GitHub 上审查和合并 PR。

## 帮助链接

- [GitHub Help](https://docs.github.com)
- [Git 官方文档](https://git-scm.com/doc)
- [Personal Access Token Guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [SSH Keys Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

**需要帮助？** 参考上述指南或访问 GitHub 官方文档。
