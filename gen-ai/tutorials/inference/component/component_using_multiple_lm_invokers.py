component = MapReduceComponent(
    lm_invoker={"map": map_invoker, "reduce": reduce_invoker},
    fallback_lms={"map": [map_backup], "reduce": [reduce_backup]},
)
