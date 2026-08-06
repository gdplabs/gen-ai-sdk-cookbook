updated_file = Attachment.from_path('path/to/updated_skill.md')
updated_skill = await lm_invoker.skill.version.create(skill.id, file=updated_file)

print(f"Created new version: {updated_skill.version}")
