import yaml
import os
from jinja2 import Template

# === 1. Lire le profil ===
with open("profiles/debug-ubuntu.yaml") as f:
    profile = yaml.safe_load(f)

# === 2. Mapper OS vers vraie image Docker ===
os_mapping = {
    "ubuntu22": "ubuntu:22.04",
    "debian12": "debian:12",
    "alpine3": "alpine:3.18"
}

os_base = os_mapping.get(profile["os"])

if not os_base:
    raise ValueError("OS non supporté")

packages = profile["packages"]

# === 3. Lire le template Dockerfile ===
with open("templates/Dockerfile.template") as f:
    template_content = f.read()

template = Template(template_content)

# === 4. Générer le Dockerfile final ===
dockerfile_content = template.render(
    os_base=os_base,
    packages=packages
)

# === 5. Créer dossier output si nécessaire ===
os.makedirs("output", exist_ok=True)

# === 6. Écrire le Dockerfile généré ===
with open("output/Dockerfile", "w") as f:
    f.write(dockerfile_content)

print("Dockerfile généré avec succès dans output/")

# ==============================
# Génération des manifests Kubernetes
# ==============================

app_name = "debug-ubuntu"
namespace = "debug-ubuntu-ns"
image = "sofiane/debug-ubuntu:v1"

# --- Deployment ---
with open("templates/deployment.yaml.template") as f:
    deployment_template = Template(f.read())

deployment_yaml = deployment_template.render(
    app_name=app_name,
    namespace=namespace,
    image=image
)

with open("output/deployment.yaml", "w") as f:
    f.write(deployment_yaml)

# --- Service ---
with open("templates/service.yaml.template") as f:
    service_template = Template(f.read())

service_yaml = service_template.render(
    app_name=app_name,
    namespace=namespace
)

with open("output/service.yaml", "w") as f:
    f.write(service_yaml)

print("Deployment et Service générés dans output/")

# ==============================
# Génération NetworkPolicies
# ==============================

with open("templates/networkpolicy.yaml.template") as f:
    np_template = Template(f.read())

networkpolicy_yaml = np_template.render(
    app_name=app_name,
    namespace=namespace
)

with open("output/networkpolicy.yaml", "w") as f:
    f.write(networkpolicy_yaml)

print("NetworkPolicies générées dans output/")
