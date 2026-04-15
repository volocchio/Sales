# Deploy this repo to VPS and sync Teams_Channel static assets.
# Usage: .\deploy.ps1 [-m "message"] [-NoPush] [-SkipTeamsSync]
param(
	[Parameter(ValueFromRemainingArguments = $true)]
	[string[]]$ForwardArgs,

	[switch]$SkipTeamsSync
)

& "$env:USERPROFILE\Dev\deploy-vps.ps1" @ForwardArgs
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
& wsl rsync -az --delete --mkpath -e "ssh -i /home/honeybadger/.ssh/id_ed25519" "$wslTeamsPath/" "root@185.164.110.65:/var/www/sales-training/Teams_Channel/"
if ($LASTEXITCODE -ne 0) {
	exit $LASTEXITCODE
}

Write-Host "Teams_Channel sync complete."
