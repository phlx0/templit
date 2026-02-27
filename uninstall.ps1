# uninstall.ps1 — remove templit completely on Windows
# Run from the repo root (or anywhere):
#   .\uninstall.ps1
#Requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$Force   # skip confirmation prompts
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── helpers ───────────────────────────────────────────────────────────────────

function Write-Ok   { param([string]$Msg) Write-Host "  $([char]0x2713) $Msg" -ForegroundColor Green }
function Write-Info { param([string]$Msg) Write-Host "  . $Msg" -ForegroundColor Cyan }
function Write-Warn { param([string]$Msg) Write-Host "  ! $Msg" -ForegroundColor Yellow }

function Confirm-Step {
    param([string]$Prompt)
    if ($Force) { return $true }
    $answer = Read-Host "  $Prompt [y/N]"
    return $answer -match "^[Yy]$"
}

function Write-Banner {
    Write-Host ""
    Write-Host "  templit uninstaller" -ForegroundColor Cyan
    Write-Host "  ──────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""
}

# ── config ────────────────────────────────────────────────────────────────────

$InstallDir = Join-Path $env:USERPROFILE ".templit"
$UserTmpl   = Join-Path $env:USERPROFILE ".config\templit"
$BinDir     = Join-Path $InstallDir "Scripts"

# ── confirm ───────────────────────────────────────────────────────────────────

Write-Banner
Write-Host "  This will remove:"
Write-Host "    $InstallDir  (virtualenv + package)" -ForegroundColor DarkGray
Write-Host "    $BinDir from your user PATH"          -ForegroundColor DarkGray
Write-Host ""

if (-not (Confirm-Step "Continue?")) {
    Write-Host "  Aborted."
    Write-Host ""
    exit 0
}
Write-Host ""

# ── remove from PATH ──────────────────────────────────────────────────────────

$UserScope   = [System.EnvironmentVariableTarget]::User
$CurrentPath = [System.Environment]::GetEnvironmentVariable("PATH", $UserScope)

if ($CurrentPath -like "*$BinDir*") {
    Write-Info "Removing $BinDir from user PATH..."
    $NewPath = ($CurrentPath -split ";" | Where-Object { $_ -ne $BinDir }) -join ";"
    [System.Environment]::SetEnvironmentVariable("PATH", $NewPath, $UserScope)
    $env:PATH = ($env:PATH -split ";" | Where-Object { $_ -ne $BinDir }) -join ";"
    Write-Ok "Removed from user PATH"
} else {
    Write-Warn "$BinDir was not found in user PATH — skipping"
}

# ── remove virtualenv ─────────────────────────────────────────────────────────

if (Test-Path $InstallDir) {
    Write-Info "Removing $InstallDir ..."
    Remove-Item -Recurse -Force $InstallDir
    Write-Ok "Removed $InstallDir"
} else {
    Write-Warn "$InstallDir not found — skipping"
}

# ── user templates (optional) ─────────────────────────────────────────────────

if (Test-Path $UserTmpl) {
    Write-Host ""
    if (Confirm-Step "Also delete your user templates at $UserTmpl?") {
        Remove-Item -Recurse -Force $UserTmpl
        Write-Ok "Removed $UserTmpl"
    } else {
        Write-Info "Kept $UserTmpl"
    }
}

# ── verify ────────────────────────────────────────────────────────────────────

Write-Host ""
$still = Get-Command templit -ErrorAction SilentlyContinue
if ($still) {
    Write-Warn "templit still found at $($still.Source) — open a new terminal to clear it from this session"
} else {
    Write-Ok "templit is no longer on PATH"
}

Write-Host ""
Write-Host "  Done." -ForegroundColor Green
Write-Host ""
