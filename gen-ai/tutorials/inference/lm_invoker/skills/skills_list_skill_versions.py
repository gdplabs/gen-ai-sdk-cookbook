versions = await lm_invoker.skill.version.list(skill.id)

for version in versions:
    print(f" - Version {version.version}: {version.metadata.get('name', 'N/A')}")
