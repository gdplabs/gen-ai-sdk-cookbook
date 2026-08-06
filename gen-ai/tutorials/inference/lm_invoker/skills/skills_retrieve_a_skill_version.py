version = await lm_invoker.skill.version.retrieve(skill.id, version="v1")

print(f"Version: {version.version}")
print(f"Metadata: {version.metadata}")
