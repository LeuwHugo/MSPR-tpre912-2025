# Réglages de base
PY            = python3
PIP           = pip
BACKEND_DIR   = backend
FRONTEND_DIR  = frontend

# ---------- targets ----------
.PHONY: dev test build deploy docs

dev:
	# Build & déploiement local des fonctions
	faas-cli up -f $(BACKEND_DIR)/stack.yml
	# Lancement du frontend en hot-reload
	cd $(FRONTEND_DIR) && npm install && npm run dev

test:
	pytest -q
	cd $(FRONTEND_DIR) && npm run test --if-present

build:
	faas-cli build -f $(BACKEND_DIR)/stack.yml
	cd $(FRONTEND_DIR) && npm run build

deploy:
	faas-cli deploy -f $(BACKEND_DIR)/stack.yml
	kubectl apply -f infra/k8s

docs:
	pandoc -s -o docs/MSPR_TPRE912.pdf docs/*.md
