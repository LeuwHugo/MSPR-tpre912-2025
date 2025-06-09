# MSPR-tpre912-2025
Mise en situation professionel numéro tpre912 réaliser dans le cadre d'une formation Master 5 à l'école EPSI 
> Preuve de concept “Serverless identité” – Juin 2025  
> École : I2 EISI · Auteur : Hugo-Reddy Leuwat-Kwetchoua

## ⚡ Stack
| Couche | Techno | Rôle |
|--------|--------|------|
| Serverless | **OpenFaaS** + K3S | Scale-to-zero |
| Fonctions | **Python 3.12** | `genPwd`, `gen2FA`, `authUser` |
| Base | **PostgreSQL 16 + pgcrypto** | Stockage hash + secrets |
| Frontend | **React + Vite** | SPA accessible (WCAG AA) |
| Observabilité | **Prometheus + Grafana** | KPI temps réel |

## 📂 Structure du dépôt
backend/ # code des fonctions FaaS

frontend/ # SPA React

infra/ # scripts K3S, Helm values

docs/ # rapport Markdown + images

.github/ # workflows CI/CD

Makefile # raccourcis build/test/deploy

## 🚀 Installation rapide
```bash
git clone <url>
cd MSPR-tpre912-2025
make dev # lance OpenFaaS + frontend hot-reload
