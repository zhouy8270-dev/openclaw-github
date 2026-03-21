$skillPaths = @(
    "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills",
    "C:\Users\Administrator\.openclaw\skills"
)

$results = @()

foreach ($skillPath in $skillPaths) {
    if (Test-Path $skillPath) {
        $skills = Get-ChildItem -Path $skillPath -Directory
        foreach ($skill in $skills) {
            $skillMd = Join-Path $skill.FullName "SKILL.md"
            $skillName = $skill.Name
            $status = ""
            
            if (-not (Test-Path $skillMd)) {
                $status = "❌ 缺少SKILL.md"
            } else {
                try {
                    $content = Get-Content $skillMd -Raw -Encoding UTF8
                    if ($content -match '^---\s*name:' -and $content -match 'description:') {
                        $status = "✅ 可用"
                    } else {
                        $status = "⚠️ YAML格式不正确"
                    }
                } catch {
                    $status = "❌ 读取失败"
                }
            }
            
            $results += [PSCustomObject]@{
                Name   = $skillName
                Status = $status
                Path   = $skill.FullName
            }
        }
    }
}

$results = $results | Sort-Object Name

# 统计
$total = $results.Count
$working = ($results | Where-Object { $_.Status -eq "✅ 可用" }).Count
$broken = ($results | Where-Object { $_.Status -ne "✅ 可用" }).Count

Write-Host "=== Skill 统计结果 ==="
Write-Host "总计: $total 个技能"
Write-Host "可用: $working 个"
Write-Host "不可用: $broken 个"
Write-Host "`n=== 详细列表 ==="
foreach ($r in $results) {
    Write-Host "$($r.Status) $($r.Name)"
}
