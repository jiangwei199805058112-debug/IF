# Windows 控制台中文乱码处理

## 1. 问题现象

在 Windows PowerShell 或 CMD 中运行 IF 控制台原型时，中文可能显示成乱码，例如菜单、场景标题或试玩记录不可读。

## 2. 原因

IF 的文本和报告使用 UTF-8。部分 Windows 控制台默认代码页不是 UTF-8，因此程序逻辑正常，但终端显示会把中文按错误编码解释。

## 3. 推荐运行方式

在 PowerShell 中进入仓库目录后运行：

```powershell
$env:PYTHONUTF8=1
chcp 65001
python -m if_game.main
```

也可以使用仓库提供的辅助脚本：

```bat
scripts\run_if_utf8.bat
```

## 4. PowerShell 临时方案

每次打开新的 PowerShell 窗口后，先执行：

```powershell
$env:PYTHONUTF8=1
chcp 65001
```

然后再运行：

```powershell
python -m if_game.main --list-scenarios
python -m if_game.main --scenario scenario_repair
```

## 5. CMD 临时方案

在 CMD 中进入仓库目录后，先执行：

```bat
chcp 65001
set PYTHONUTF8=1
python -m if_game.main
```

也可以直接双击或运行：

```bat
scripts\run_if_utf8.bat
```

## 6. 不建议做的事

不建议为了运行当前原型修改系统全局语言设置。
不建议为了游戏修改注册表。
不建议在程序里强制修改系统编码。
当前乱码只影响显示，不影响程序逻辑和测试。
