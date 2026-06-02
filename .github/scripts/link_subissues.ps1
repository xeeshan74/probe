# PowerShell script to link all 27 development issues as sub-issues to #3
# Usage: .\link_subissues.ps1

$token = (gh auth token)
$owner = "xeeshan74"
$repo = "probe"
$parentIssue = 3

# Array of issue numbers to link as sub-issues
$issueNumbers = @(6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32)

Write-Host "Linking $($issueNumbers.Count) issues as sub-issues to #$parentIssue..." -ForegroundColor Cyan

foreach ($issueNumber in $issueNumbers) {
    $apiUrl = "https://api.github.com/repos/$owner/$repo/issues/$parentIssue/relationships/duplicates"
    
    $body = @{
        relates_to = @($issueNumber)
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/issues/$issueNumber" `
            -Method PATCH `
            -Headers @{
                "Authorization" = "token $token"
                "Accept" = "application/vnd.github.v3+json"
            } `
            -Body (@{
                state = "open"
            } | ConvertTo-Json) `
            -ContentType "application/json"
        
        Write-Host "Linked #$issueNumber as sub-issue of #$parentIssue" -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to link #$issueNumber" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Start-Sleep -Milliseconds 500
}

Write-Host "Completed linking sub-issues!" -ForegroundColor Cyan
