# 一键更新 leeon 素材库网站：重建页面 + 同步资源 + 提交推送
$ErrorActionPreference = "Stop"
$site = "D:\AI\codex\projects\leeon账号运营\leeon\素材库网站"

Push-Location $site
try {
    git config http.proxy http://127.0.0.1:10809

    Write-Host "[1/3] 重建 index.html ..." -ForegroundColor Cyan
    python build_site.py
    if ($LASTEXITCODE -ne 0) { throw "build_site.py 失败" }

    Write-Host "[2/3] 提交变更 ..." -ForegroundColor Cyan
    git add -A
    git commit -m "素材库更新 $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -q

    Write-Host "[3/3] 推送到 GitHub ..." -ForegroundColor Cyan
    git push -q
    Write-Host "完成！等待 1-2 分钟 Pages 生效。" -ForegroundColor Green
} finally {
    Pop-Location
}
