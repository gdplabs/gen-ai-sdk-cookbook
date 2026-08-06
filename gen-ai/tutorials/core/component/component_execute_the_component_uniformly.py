formatter = TextFormatter()

result = await formatter.run(text="hello", uppercase=True, repeat=2)
assert result == "HELLOHELLO"
