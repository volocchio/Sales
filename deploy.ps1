# Deploy this repo to VPS and sync static assets.
#
# Strategy: commit + push from local, then have the VPS pull and copy
# tracked files server-side. We do NOT rsync large binary asset folders
# from WSL — the WSL2 NAT chokes on multi-GB SSH transfers (broken pipe).
# Instead the VPS hosts a clone of the repo at $REPO_VPS, runs `git pull`,
# and we cp tracked files into the served directory locally on the VPS.
#
# Usage: .\deploy.ps1 [-m "message"] [-NoPush] [-SkipAssetSync]
param(
	[Alias('m')]
	[string]$Message = "deploy $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
	[switch]$NoPush,
	[Alias('SkipTeamsSync')]
	[switch]$SkipAssetSync
)

$ErrorActionPreference = 'Stop'

$VPS = "root@185.164.110.65"
$SSH_KEY = "/home/honeybadger/.ssh/id_ed25519"
$REPO_VPS = "/root/.openclaw/workspace-tag_coding/Sales"
$SITE_DIR = "/var/www/sales-training"
$PORTAL_SYNC = "/usr/local/bin/sync-and-update-portal.sh"

function Invoke-RemoteBash {
	param([string]$Script)
	# Pass script via base64 over stdin to dodge nested-quoting hell.
	$encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Script))
	& wsl ssh -i $SSH_KEY $VPS "echo $encoded | base64 -d | bash"
	return $LASTEXITCODE
}

# 1. Commit + push local changes.
if (-not $NoPush) {
	$status = git status --porcelain
	if ($status) {
		Write-Host "Committing local changes..."
		git add -A
		git commit -m $Message
		if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
	}
	else {
		Write-Host "No local changes to commit."
	}

	Write-Host "Pushing to origin..."
	git push
	if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
else {
	Write-Host "Skipping git push (-NoPush)."
}

# 2. On VPS: pull repo, copy tracked files into served directory.
Write-Host "Updating VPS repo and copying tracked files into $SITE_DIR..."

$copyCmd = if ($SkipAssetSync) {
	"echo 'Skipping asset folder copy (-SkipAssetSync).'"
}
else {
	# Single-quoted here-string: nothing interpolated. We inject $SITE_DIR
	# via -replace at the end.
	@'
git ls-files -z | tr '\0' '\n' | grep -E '^(Teams_Channel|Sales and Marketing|Aircraft Models|Shared Resources|Training|Presentations)/' > /tmp/sales_assets.list
COUNT=$(wc -l < /tmp/sales_assets.list)
echo "Tracked asset files: $COUNT"
# No --delete: preserve VPS-only files (e.g. the 3.4GB of Teams_Channel
# binaries that aren't tracked because they exceed git's size limit).
rsync -a --files-from=/tmp/sales_assets.list ./ '__SITE_DIR__/'
'@ -replace '__SITE_DIR__', $SITE_DIR
}

# Build remote script with single-quoted here-string + token replacement.
$remote = @'
set -e
cd __REPO_VPS__
git fetch --all --prune -q
git reset --hard origin/main -q
echo "VPS now at: $(git log --oneline -1)"

# Copy top-level static files (HTML, mjs, package*.json) into site dir
cp -f *.html *.mjs package*.json '__SITE_DIR__/' 2>/dev/null || true

__COPY_CMD__
echo "Site update complete."
'@
$remote = $remote -replace '__REPO_VPS__', $REPO_VPS
$remote = $remote -replace '__SITE_DIR__', $SITE_DIR
$remote = $remote -replace '__COPY_CMD__', $copyCmd

$exit = Invoke-RemoteBash -Script $remote
if ($exit -ne 0) { exit $exit }

# 3. Trigger portal index regeneration.
Write-Host "Running portal sync..."
$exit = Invoke-RemoteBash -Script "$PORTAL_SYNC"
if ($exit -ne 0) {
	Write-Warning "Portal sync exited $exit (non-fatal)."
}

Write-Host "Deploy complete."
