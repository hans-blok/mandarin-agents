param(
    [Parameter(Mandatory=$true)]
    [string]$Agent,
    
    [Parameter(Mandatory=$true)]
    [string]$Intent,
    
    [Parameter(Mandatory=$true)]
    [string]$TargetAgent,
    
    [Parameter(Mandatory=$true)]
    [string]$ValueStreamFase,
    
    [Parameter(Mandatory=$true)]
    [string]$Beschrijving
)

# Find workspace root (current directory when called from VSCode task)
$workspaceRoot = $PWD

$generator = Join-Path $workspaceRoot 'scripts/generate_instructions.py'
$timestamp = Get-Date -Format 'yyyyMMddHHmmss'
$hashInput = $timestamp + $Agent
$md5 = [System.Security.Cryptography.MD5]::Create()
$hashBytes = $md5.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($hashInput))
$hash = [System.BitConverter]::ToString($hashBytes).Replace('-','').Substring(0,4).ToLower()
$filename = "agent-execution/$hash.$Agent.$Intent.md"

# Execute
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'

python $generator --agent $Agent --intent $Intent -p agent_naam=$TargetAgent -p value_stream_fase=$ValueStreamFase -p korte_beschrijving=$Beschrijving --execution-file $filename

if ($LASTEXITCODE -eq 0) {
    code $filename
}
