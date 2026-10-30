Add-Type -AssemblyName System.Windows.Forms
$ErrorActionPreference = 'Stop'
$picker = New-Object System.Windows.Forms.OpenFileDialog
$picker.Title = '스페이스 코브라 II v0.81 - 일본판 원본 CUE 선택'
$picker.Filter = 'CUE 디스크 이미지 (*.cue)|*.cue'
if ($picker.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 0 }
$sourceCue = $picker.FileName
$sourceFolder = [System.IO.Path]::GetDirectoryName($sourceCue)
$outputFolder = $sourceFolder + ' [KO v0.81]'
Write-Host ('출력 폴더: ' + $outputFolder)
Write-Host '원본 검사와 패치 적용 후 결과 해시를 확인합니다. 완료될 때까지 기다려 주세요.'
& (Join-Path $PSScriptRoot 'Cobra2PatchApplier.exe') $sourceCue $outputFolder
$resultCode = $LASTEXITCODE
if ($resultCode -eq 0) {
    [System.Windows.Forms.MessageBox]::Show(('패치 완료!' + [Environment]::NewLine + (Join-Path $outputFolder 'cobra2-ko-experimental.cue')), '코브라 II v0.81') | Out-Null
} else {
    [System.Windows.Forms.MessageBox]::Show('패치에 실패했습니다. 콘솔의 오류와 지원 원본 해시를 확인해 주세요. 기존 출력이 있으면 새 출력 경로를 사용하세요.', '코브라 II v0.81') | Out-Null
}
exit $resultCode
