$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
Write-Host "Proxy enabled: $env:HTTP_PROXY"

# 验证代理是否设置成功（返回200则成功）
$response = curl -s -o /dev/null -w "%{http_code}\n" -m 3 https://www.google.com

# 检查 curl 命令的退出码
if ($response -eq 200) {
    Write-Host "成功访问 Google"
}else{
    Write-Host "无法访问 Google"
}
