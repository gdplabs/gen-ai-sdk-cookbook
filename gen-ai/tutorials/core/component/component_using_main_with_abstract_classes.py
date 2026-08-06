upper = UpperCaseProcessor()
lower = LowerCaseProcessor()

result1 = await upper.run(data="hello")  # Returns "HELLO"
result2 = await lower.run(data="WORLD")  # Returns "world"
