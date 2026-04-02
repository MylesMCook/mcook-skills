param(
  [Parameter(Mandatory = $true)]
  [string]$Url,

  [Parameter(Mandatory = $true)]
  [string]$OutDir,

  [string]$Scenario = "smoke"
)

$runId = "$(Get-Date -Format yyyyMMdd-HHmmss)-$([guid]::NewGuid().ToString('N').Substring(0,4))"
$env:AGENT_BROWSER_SESSION = "$Scenario-$runId"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

agent-browser open $Url
agent-browser wait 1500
agent-browser snapshot -i --json
agent-browser screenshot (Join-Path $OutDir "$Scenario.png")
agent-browser get url
agent-browser get title
agent-browser errors
