# Azure access for teammates — troubleshooting

**Subscription:** `79022606-988b-4679-9a0e-18fd3351d77a`  
**Tenant (switch to this in portal):** `ztajischoolberkeley.onmicrosoft.com`  
**Resource group:** `capstone-295`  
**Live app:** https://probe-capstone295.azurewebsites.net

---

## Brian’s 401 in Microsoft Entra ID — expected

**Contributor on a resource group does not grant Entra ID admin access.** The 401 with empty `subscriptionId` in Entra ID is normal for teammates.

| Task | Use this | Not this |
|------|----------|----------|
| Deploy code | **GitHub Actions** (below) or `az webapp deploy` | Entra ID portal |
| View app resources | Azure Portal → **capstone-295** | Entra ID → Users |
| Manage tenant users | Owner only | — |

---

## DevOps for Brian — GitHub Actions (easiest)

1. Go to https://github.com/xeeshan74/probe  
2. **Actions** → **Deploy PROBE to Azure** → **Run workflow**  
3. Or merge/push to **`main`** — deploy runs automatically  

**Secret `AZURE_WEBAPP_PUBLISH_PROFILE` is configured** (owner set this up).

Brian’s GitHub login: **`briantwai`** — already a collaborator.

---

## Azure Portal (if needed)

1. Top-right → **Switch directory** → **Default Directory** (`ztajischoolberkeley.onmicrosoft.com`)  
2. Open: https://portal.azure.com/#@ztajischoolberkeley.onmicrosoft.com/resource/subscriptions/79022606-988b-4679-9a0e-18fd3351d77a/resourceGroups/capstone-295/overview  
3. Click **probe-capstone295** for logs, config, restart  

---

## Azure CLI (alternative)

```powershell
az logout
az login
az account set --subscription "79022606-988b-4679-9a0e-18fd3351d77a"
az group show -n capstone-295
```

Deploy: see [README.md](./README.md).

---

## Verified Contributor assignments

| Teammate | Email |
|----------|-------|
| Brian | brian_wai@ischool.berkeley.edu |
| Abdul | hardiumar@ischool.berkeley.edu |
| Pauline | pauline.chane@ischool.berkeley.edu |

Re-invite: `.\add-teammate.ps1 email@ischool.berkeley.edu`
