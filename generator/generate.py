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
