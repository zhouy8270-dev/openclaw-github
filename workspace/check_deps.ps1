$skillPaths = @(
    "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills",
    "C:\Users\Administrator\.openclaw\skills"
)

$results = @()

function Test-Command($cmd) {
    try {
        Get-Command $cmd -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

foreach ($skillPath in $skillPaths) {
    if (Test-Path $skillPath) {
        $skills = Get-ChildItem -Path $skillPath -Directory
        foreach ($skill in $skills) {
            $skillMd = Join-Path $skill.FullName "SKILL.md"
            $skillName = $skill.Name
            $formatOk = $false
            $depsOk = $true
            $missingDeps = @()
            
            if (-not (Test-Path $skillMd)) {
                $formatStatus = "❌ 缺少SKILL.md"
                $formatOk = $false
            } else {
                try {
                    $content = Get-Content $skillMd -Raw -Encoding UTF8
                    if ($content -match '^---\s*name:' -and $content -match 'description:') {
                        $formatStatus = "✅ 格式正确"
                        $formatOk = $true
                        
                        # 提取requires.bins
                        if ($content -match 'requires:\s*\{\s*bins\s*:\s*\[(.*?)\]') {
                            $binsMatch = $matches[1]
                            $bins = $binsMatch -split ',' | ForEach-Object { 
                                $b = $_ -replace '"|\s', ''
                                if (-not [string]::IsNullOrWhiteSpace($b)) { $b }
                            }
                            foreach ($bin in $bins) {
                                if (-not (Test-Command $bin)) {
                                    $depsOk = $false
                                    $missingDeps += $bin
                                }
                            }
                        }
                    } else {
                        $formatStatus = "⚠️ YAML格式不正确"
                        $formatOk = $false
                    }
                } catch {
                    $formatStatus = "❌ 读取失败"
                    $formatOk = $false
                }
            }
            
            if (-not $formatOk) {
                $overallStatus = "❌ 不可用"
            } elseif ($depsOk) {
                $overallStatus = "✅ 可用"
            } else {
                $overallStatus = "⚠️ 依赖缺失"
            }
            
            $results += [PSCustomObject]@{
                Name         = $skillName
                FormatStatus = $formatStatus
                DepsStatus   = if ($depsOk) { "✅ 依赖满足" } else { "⚠️ 缺少依赖: $($missingDeps -join ', ')" }
                Overall      = $overallStatus
                Missing      = $($missingDeps -join ', ')
            }
        }
    }
}

$results = $results | Sort-Object Name

Write-Host "=== Skill 可用性统计 (Windows环境) ==="
$total = $results.Count
$available = ($results | Where-Object { $_.Overall -eq "✅ 可用" }).Count
$missingDeps = ($results | Where-Object { $_.Overall -eq "⚠️ 依赖缺失" }).Count
$unavailable = ($results | Where-Object { $_.Overall -eq "❌ 不可用" }).Count

Write-Host "总计: $total 个技能"
Write-Host "✅ 完全可用: $available 个"
Write-Host "⚠️ 依赖缺失: $missingDeps 个"
Write-Host "❌ 格式损坏: $unavailable 个"
Write-Host "`n=== 详细列表 ==="

foreach ($r in $results) {
    Write-Host "$($r.Overall) $($r.Name)"
    if ($r.Missing) {
        Write-Host "     ↳ 缺少: $($r.Missing)"
    }
}
