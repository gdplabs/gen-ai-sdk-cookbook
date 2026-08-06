formatter = TextFormatter()
ParamsModel = formatter.input_params  # type: ignore[attr-defined]

params = ParamsModel(text="world", repeat=2)
result = await formatter.run(**params.model_dump())
