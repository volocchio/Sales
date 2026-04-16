# Deploy this repo to VPS and sync static assets.
# Usage: .\deploy.ps1 [-m "message"] [-NoPush] [-SkipTeamsSync]
param(
	[Parameter(ValueFromRemainingArguments = $true)]
	[string[]]$ForwardArgs,

	[switch]$SkipTeamsSync
)

$SSH = "ssh -i /home/honeybadger/.ssh/id_ed25519 -o ServerAliveInterval=30 -o ServerAliveCountMax=10"
$VPS = "root@185.164.110.65"
$REPO_VPS = "/root/.openclaw/workspace-tag_coding/Sales"
$SITE_DIR = "/var/www/sales-training"

& "$env:USERPROFILE\Dev\deploy-vps.ps1" @ForwardArgs
if ($LASTEXITCODE -ne 0) {
	exit $LASTEXITCODE
}

# Copy HTML + static files from the git repo to the served directory
Write-Host "Syncing HTML files from git repo to static site..."
& wsl ssh -i /home/honeybadger/.ssh/id_ed25519 $VPS "cp $REPO_VPS/*.html $REPO_VPS/*.mjs $REPO_VPS/package*.json $SITE_DIR/ 2>/dev/null; echo ok"
if ($LASTEXITCODE -ne 0) {
	exit $LASTEXITCODE
}

if ($SkipTeamsSync) {
	Write-Host "Skipping Teams_Channel sync (-SkipTeamsSync)."
	exit 0
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$teamsPath = Join-Path $repoRoot "Teams_Channel"

if (-not (Test-Path -LiteralPath $teamsPath)) {
	Write-Warning "Teams_Channel folder not found at: $teamsPath"
	exit 0
}

$drive = $teamsPath.Substring(0, 1).ToLower()
$rest = $teamsPath.Substring(2) -replace '\\', '/'
$wslTeamsPath = "/mnt/$drive$rest"

Write-Host "Syncing Teams_Channel to VPS static site..."
& wsl rsync -az --delete --mkpath -e "$SSH" "$wslTeamsPath/" "${VPS}:${SITE_DIR}/Teams_Channel/"
if ($LASTEXITCODE -ne 0) {
	exit $LASTEXITCODE
}

Write-Host "Deploy complete."
