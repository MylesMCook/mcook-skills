param(
  [Parameter(Mandatory = $true)]
  [string]$Url,

  [string]$SessionPrefix = "probe"
)

$runId = "$(Get-Date -Format yyyyMMdd-HHmmss)-$([guid]::NewGuid().ToString('N').Substring(0,4))"
$env:AGENT_BROWSER_SESSION = "$SessionPrefix-$runId"

Write-Host "AGENT_BROWSER_SESSION=$env:AGENT_BROWSER_SESSION"
agent-browser open $Url
agent-browser snapshot -i --json
agent-browser get url
agent-browser get title
