Remove-Item Env:HTTP_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:HTTPS_PROXY -ErrorAction SilentlyContinue
Write-Host "Proxy disabled."
# 执行 curl 命令并设置超时时间为5秒
curl -s -o NUL -w "%{http_code}\n" -m 3 https://www.google.com

# 检查 curl 命令的退出码
if ($LASTEXITCODE -ne 0) {
    Write-Host "无法访问google"
}
