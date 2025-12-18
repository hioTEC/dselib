f# WSL 403错误一键修复脚本
# 管理员权限运行此脚本

Write-Host "开始修复WSL 403错误..." -ForegroundColor Green

# 检查是否以管理员权限运行
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "请以管理员权限运行此脚本！" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit
}

Write-Host "✓ 管理员权限验证通过" -ForegroundColor Green

# 步骤1: 重置Microsoft Store缓存
Write-Host "步骤1: 重置Microsoft Store缓存..." -ForegroundColor Yellow
try {
    Start-Process "wsreset.exe" -Wait
    Write-Host "✓ Microsoft Store缓存重置完成" -ForegroundColor Green
} catch {
    Write-Host "✗ Microsoft Store缓存重置失败" -ForegroundColor Red
}

# 步骤2: 启用WSL功能
Write-Host "步骤2: 启用WSL相关功能..." -ForegroundColor Yellow

# 启用Windows Subsystem for Linux
Write-Host "  - 启用Windows Subsystem for Linux..." -ForegroundColor Cyan
try {
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    Write-Host "  ✓ WSL功能启用成功" -ForegroundColor Green
} catch {
    Write-Host "  ✗ WSL功能启用失败" -ForegroundColor Red
}

# 启用虚拟机平台
Write-Host "  - 启用虚拟机平台..." -ForegroundColor Cyan
try {
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    Write-Host "  ✓ 虚拟机平台启用成功" -ForegroundColor Green
} catch {
    Write-Host "  ✗ 虚拟机平台启用失败" -ForegroundColor Red
}

# 步骤3: 检查网络连接
Write-Host "步骤3: 检查网络连接..." -ForegroundColor Yellow
try {
    $connection = Test-NetConnection -ComputerName "www.microsoft.com" -Port 443 -InformationLevel Quiet
    if ($connection) {
        Write-Host "✓ Microsoft服务器连接正常" -ForegroundColor Green
    } else {
        Write-Host "✗ 无法连接到Microsoft服务器" -ForegroundColor Red
        Write-Host "  请检查网络连接和代理设置" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ 网络连接测试失败" -ForegroundColor Red
}

# 步骤4: 设置WSL2为默认版本
Write-Host "步骤4: 设置WSL2为默认版本..." -ForegroundColor Yellow
try {
    wsl --set-default-version 2
    Write-Host "✓ WSL2设置为默认版本" -ForegroundColor Green
} catch {
    Write-Host "✗ 设置WSL2默认版本失败" -ForegroundColor Red
}

# 步骤5: 检查Windows更新
Write-Host "步骤5: 检查Windows更新..." -ForegroundColor Yellow
try {
    Write-Host "  建议手动运行Windows Update检查更新" -ForegroundColor Cyan
    Write-Host "  设置 -> 更新和安全 -> Windows Update" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Windows更新检查建议失败" -ForegroundColor Red
}

# 步骤6: 提供手动下载链接
Write-Host "步骤6: 提供手动下载链接..." -ForegroundColor Yellow
Write-Host "如果上述步骤仍无法解决问题，请手动下载以下文件：" -ForegroundColor Cyan
Write-Host "  1. WSL2 Linux内核更新包: https://aka.ms/wsl2kernel" -ForegroundColor White
Write-Host "  2. Ubuntu应用包: https://www.microsoft.com/store/p/ubuntu/9nblggh4msv6" -ForegroundColor White

# 步骤7: 安装WSL
Write-Host "步骤7: 尝试安装WSL..." -ForegroundColor Yellow
try {
    wsl --install
    Write-Host "✓ WSL安装命令已执行" -ForegroundColor Green
    Write-Host "请重启计算机后重新运行 wsl --install 命令" -ForegroundColor Cyan
} catch {
    Write-Host "✗ WSL安装失败，请重启后手动运行: wsl --install" -ForegroundColor Red
}

# 最终建议
Write-Host "`n修复脚本执行完成！" -ForegroundColor Green
Write-Host "建议的步骤：" -ForegroundColor Yellow
Write-Host "1. 重启计算机" -ForegroundColor White
Write-Host "2. 以管理员身份打开PowerShell" -ForegroundColor White
Write-Host "3. 运行: wsl --install" -ForegroundColor White
Write-Host "4. 如果仍有问题，使用手动下载方法" -ForegroundColor White

Write-Host "`n按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
