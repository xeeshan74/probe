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
} | ConvertTo-Json | Set-Content $tmp -Encoding utf8

Write-Host "Inviting $email..."
$invite = az rest --method POST --uri "https://graph.microsoft.com/v1.0/invitations" `
  --headers "Content-Type=application/json" --body "@$tmp" | ConvertFrom-Json

$objectId = $invite.invitedUser.id
Write-Host "Assigning Contributor on capstone-295..."
az role assignment create --assignee-object-id $objectId --assignee-principal-type User `
  --role Contributor --scope $SCOPE | Out-Null

Write-Host "Done. $email must accept the Azure invitation email before portal access works."
