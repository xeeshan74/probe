# Azure deploy — PROBE (capstone-295)

**Resource group:** `capstone-295` · **Region:** eastus  
**Subscription:** Azure for Students · `79022606-988b-4679-9a0e-18fd3351d77a`

---

## Live URL (App Service — F1 free)

**https://probe-capstone295.azurewebsites.net**

| Resource | Name |
|----------|------|
| Resource group | `capstone-295` |
| App Service plan | `capstone-295-plan` (Linux F1) |
| Web app | `probe-capstone295` |

VM `probe-vm` was **not** created — student subscription has **zero VM core quota** in eastus. App Service works as the cheap hosted option (free tier limits apply).

---

## Start / stop costs

| Resource | When idle |
|----------|-----------|
| **F1 App Service** | Free tier — CPU/time limits; app may sleep when idle |
| **VM (future)** | `az vm deallocate` stops compute billing; disk ~$3–5/mo |

To **stop** App Service (save free-tier minutes):

```powershell
az webapp stop --resource-group capstone-295 --name probe-capstone295
```

To **start** before demo:

```powershell
az webapp start --resource-group capstone-295 --name probe-capstone295
```

---

## Redeploy after code changes

From `probe/` folder:

```powershell
Compress-Archive -Path app.py,requirements.txt,assessment_controller.py,authorization.py,chart_help.py,charts.py,config.py,discovery.py,dns_utils.py,email_checks.py,models.py,page_classifier.py,report_generator.py,risk_engine.py,storage.py,tls_checks.py,web_checks.py,__init__.py,utils,.streamlit -DestinationPath deploy.zip -Force

az webapp deploy --resource-group capstone-295 --name probe-capstone295 --src-path deploy.zip --type zip
```

Startup command (already set):

```text
python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false
```

**WebSockets must be enabled** (Streamlit requires them behind Azure’s proxy):

```powershell
az webapp config set --resource-group capstone-295 --name probe-capstone295 --web-sockets-enabled true
```

Include `.streamlit/config.toml` in the deploy zip (proxy/CORS settings for App Service).

---

## Add teammates (Contributor)

Run once per teammate email (Brian, Abdul, Pauline):

```powershell
$SCOPE = "/subscriptions/79022606-988b-4679-9a0e-18fd3351d77a/resourceGroups/capstone-295"

az role assignment create --assignee TEAMMATE@berkeley.edu --role Contributor --scope $SCOPE
```

They accept the Azure invite, then can redeploy, start/stop the web app, and (after VM quota) manage the VM.

---

## Linux VM (optional — after quota increase)

Request **1–2 cores** for **Standard BS Family** in **eastus**:  
[Azure quotas blade](https://portal.azure.com/#view/Microsoft_Azure_Capacity/QuotaMenuBlade/~/myQuotas)

Then:

```powershell
az vm create --resource-group capstone-295 --name probe-vm --location eastus `
  --image Ubuntu2204 --size Standard_B1s --admin-username azureuser `
  --ssh-key-values "$env:USERPROFILE\.ssh\id_rsa.pub" --public-ip-sku Standard `
  --tags Project=PROBE Capstone=295

az vm open-port --resource-group capstone-295 --name probe-vm --port 8501 --priority 1010

az vm run-command invoke --resource-group capstone-295 --name probe-vm `
  --command-id RunShellScript --scripts "@install-probe.sh"
```

Install script: [install-probe.sh](./install-probe.sh)

---

## Portal

[capstone-295 resource group](https://portal.azure.com/#@ztajischoolberkeley.onmicrosoft.com/resource/subscriptions/79022606-988b-4679-9a0e-18fd3351d77a/resourceGroups/capstone-295/overview)

---

## Tags

`Project=PROBE` · `Capstone=295`
