# install.ps1 — install templit on Windows
# Run from the repo root:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#   .\install.ps1
#Requires -Version 5.1
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── helpers ───────────────────────────────────────────────────────────────────

function Write-Ok   { param([string]$Msg) Write-Host "  $([char]0x2713) $Msg" -ForegroundColor Green }
function Write-Err  { param([string]$Msg) Write-Host "  $([char]0x2717) $Msg" -ForegroundColor Red; exit 1 }
function Write-Info { param([string]$Msg) Write-Host "  . $Msg" -ForegroundColor Cyan }
function Write-Warn { param([string]$Msg) Write-Host "  ! $Msg" -ForegroundColor Yellow }

function Write-Banner {
    Write-Host ""
    Write-Host "  templit installer" -ForegroundColor Cyan
    Write-Host "  ──────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""
}

# ── config ────────────────────────────────────────────────────────────────────

$InstallDir = Join-Path $env:USERPROFILE ".templit"
$ScriptDir  = $PSScriptRoot

# ── checks ────────────────────────────────────────────────────────────────────

Write-Banner
Write-Info "Checking requirements..."

$PythonCmd = $null
foreach ($candidate in @("python", "python3", "py")) {
    try {
        $ver = & $candidate --version 2>&1
        if ($ver -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 9) {
                $PythonCmd = $candidate
                Write-Ok "Python $major.$minor ($candidate)"
                break
            }
        }
    } catch { <# not found, try next #> }
}

if (-not $PythonCmd) {
    Write-Err "Python 3.9+ not found. Download it from https://python.org"
}

# ── virtualenv ────────────────────────────────────────────────────────────────

Write-Info "Creating virtualenv at $InstallDir ..."
if (Test-Path $InstallDir) {
    Write-Warn "Directory $InstallDir already exists — reinstalling into it."
}

& $PythonCmd -m venv $InstallDir
if ($LASTEXITCODE -ne 0) { Write-Err "Failed to create virtualenv." }
Write-Ok "Virtualenv ready"

# ── install package ───────────────────────────────────────────────────────────

$Pip     = Join-Path $InstallDir "Scripts\pip.exe"
$Python  = Join-Path $InstallDir "Scripts\python.exe"

Write-Info "Upgrading pip..."
& $Pip install --quiet --upgrade pip
if ($LASTEXITCODE -ne 0) { Write-Err "pip upgrade failed." }

Write-Info "Installing templit..."
& $Pip install --quiet -e $ScriptDir
if ($LASTEXITCODE -ne 0) { Write-Err "templit installation failed." }
Write-Ok "Package installed"

# ── add to PATH ───────────────────────────────────────────────────────────────

$BinDir    = Join-Path $InstallDir "Scripts"
$UserScope = [System.EnvironmentVariableTarget]::User
$CurrentPath = [System.Environment]::GetEnvironmentVariable("PATH", $UserScope)

if ($CurrentPath -notlike "*$BinDir*") {
    Write-Info "Adding $BinDir to user PATH..."
    [System.Environment]::SetEnvironmentVariable(
        "PATH",
        "$BinDir;$CurrentPath",
        $UserScope
    )
    Write-Ok "Added to user PATH"
    Write-Warn "Open a new terminal for the PATH change to take effect."
} else {
    Write-Ok "$BinDir is already in user PATH"
}

# also update the current session
$env:PATH = "$BinDir;$env:PATH"

# ── done ──────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "  All done! " -ForegroundColor Green -NoNewline
Write-Host "Run: " -NoNewline
Write-Host "templit list" -ForegroundColor White
Write-Host "  (or open a new terminal if the command isn't found yet)" -ForegroundColor DarkGray
Write-Host ""
