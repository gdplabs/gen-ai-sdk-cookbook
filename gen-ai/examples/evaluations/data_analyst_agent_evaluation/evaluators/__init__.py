"""Evaluator registry for query-specific evaluation logic."""

from .base import BaseQueryEvaluator
from .query_evaluator_001 import QueryEvaluator001
from .query_evaluator_002 import QueryEvaluator002
from .query_evaluator_003 import QueryEvaluator003
from .query_evaluator_004 import QueryEvaluator004
from .query_evaluator_005 import QueryEvaluator005
from .query_evaluator_006 import QueryEvaluator006
from .query_evaluator_007 import QueryEvaluator007
from .query_evaluator_008 import QueryEvaluator008
from .query_evaluator_009 import QueryEvaluator009
from .query_evaluator_010 import QueryEvaluator010
from .query_evaluator_011 import QueryEvaluator011
from .query_evaluator_012 import QueryEvaluator012
from .query_evaluator_013 import QueryEvaluator013
from .query_evaluator_014 import QueryEvaluator014
from .query_evaluator_015 import QueryEvaluator015
from .query_evaluator_016 import QueryEvaluator016
from .query_evaluator_017 import QueryEvaluator017
from .query_evaluator_018 import QueryEvaluator018
from .query_evaluator_019 import QueryEvaluator019
from .query_evaluator_020 import QueryEvaluator020
from .query_evaluator_021 import QueryEvaluator021
from .query_evaluator_022 import QueryEvaluator022
from .query_evaluator_023 import QueryEvaluator023

EVALUATORS: dict[int, type[BaseQueryEvaluator]] = {
    cls.QUERY_ID: cls
    for cls in [
        QueryEvaluator001,
        QueryEvaluator002,
        QueryEvaluator003,
        QueryEvaluator004,
        QueryEvaluator005,
        QueryEvaluator006,
        QueryEvaluator007,
        QueryEvaluator008,
        QueryEvaluator009,
        QueryEvaluator010,
        QueryEvaluator011,
        QueryEvaluator012,
        QueryEvaluator013,
        QueryEvaluator014,
        QueryEvaluator015,
        QueryEvaluator016,
        QueryEvaluator017,
        QueryEvaluator018,
        QueryEvaluator019,
        QueryEvaluator020,
        QueryEvaluator021,
        QueryEvaluator022,
        QueryEvaluator023,
    ]
}
