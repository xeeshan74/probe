# Invite a teammate to capstone-295 (guest user + Contributor role)
# Usage: .\add-teammate.ps1 teammate@ischool.berkeley.edu

$ErrorActionPreference = "Stop"

$SCOPE = "/subscriptions/79022606-988b-4679-9a0e-18fd3351d77a/resourceGroups/capstone-295"

if (-not $args[0]) {
  Write-Host "Usage: .\add-teammate.ps1 teammate@ischool.berkeley.edu"
  exit 1
}

$email = $args[0]
$tmp = Join-Path $env:TEMP "azure-invite.json"

@{
  invitedUserEmailAddress = $email
  inviteRedirectUrl       = "https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups"
  sendInvitationMessage   = $true
  invitedUserMessageInfo  = @{
    messageLanguage       = "en-US"
    customizedMessageBody = @(
      "You have been invited to collaborate on the PROBE capstone project (Cybersecurity 295)."
      "Accept this invitation to access the shared Azure resource group capstone-295 and help manage the PROBE app."
      "Live demo: https://probe-capstone295.azurewebsites.net"
    ) -join " "
  }
} | ConvertTo-Json -Depth 4 | Set-Content $tmp -Encoding utf8

Write-Host "Inviting $email (US English)..."
$inviteJson = az rest --method POST --uri "https://graph.microsoft.com/v1.0/invitations" `
  --headers "Content-Type=application/json" --body "@$tmp" 2>&1
if ($LASTEXITCODE -ne 0) {
  Write-Error $inviteJson
}
$invite = $inviteJson | ConvertFrom-Json

$objectId = $invite.invitedUser.id
Write-Host "Assigning Contributor on capstone-295..."
$assignJson = az role assignment create --assignee-object-id $objectId --assignee-principal-type User `
  --role Contributor --scope $SCOPE 2>&1
if ($LASTEXITCODE -ne 0 -and $assignJson -notmatch "already exists") {
  Write-Error $assignJson
}

Write-Host "Done. $email must accept the Azure invitation email before portal access works."
