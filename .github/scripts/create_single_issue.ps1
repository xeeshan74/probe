# PowerShell script to create the remaining PDF/HTML report export issue

$token = (gh auth token)
$owner = "xeeshan74"
$repo = "probe"
$apiUrl = "https://api.github.com/repos/$owner/$repo/issues"

$issue = @{
    title = "[Stretch][P2] PDF / HTML report export"
    body = "Implement PDF and HTML report export functionality.`n`n(WBS P2)`nNotes: Markdown is MVP"
    labels = @("P2", "stretch")
    assignees = @("ghostfruitleaf")
}

$body = @{
    title = $issue.title
    body = $issue.body
    labels = $issue.labels
    assignees = $issue.assignees
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $apiUrl `
        -Method POST `
        -Headers @{
            "Authorization" = "token $token"
            "Accept" = "application/vnd.github.v3+json"
        } `
        -Body $body `
        -ContentType "application/json"
    
    Write-Host "Created: $($issue.title)" -ForegroundColor Green
}
catch {
    Write-Host "Failed: $($issue.title)" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
