skills = await lm_invoker.skill.list()

if not skills:
    print("No skills found.")

for skill in skills:
    print(f" - {skill.id}: {skill.skill_type} (version: {skill.version})")
