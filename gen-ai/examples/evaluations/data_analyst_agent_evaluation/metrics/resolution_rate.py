"""Resolution rate metric.

Author:
    - Mikhael Chris (mikhael.chris@gdplabs.id)
"""

from collections.abc import Callable

import pandas as pd

import logging

logger = logging.getLogger(__name__)


def _safe_assert(
    assertion: Callable[[str, dict], bool],
    code: str,
    namespace: dict,
) -> bool:
    """Run assertion(code, namespace), treating AssertionError as False."""
    try:
        return bool(assertion(code, namespace))
    except AssertionError as e:
        logger.info(f"ResolutionRateMetric assertion failed: {e}")
        return False
    except Exception as e:
        logger.warning(f"ResolutionRateMetric assertion raised: {e}")
        return False


class ResolutionRateMetric:
    r"""Resolution Rate metric.

    Pure evaluation metric that receives a single code string, a DataFrame,
    and an assertion callable. Executes the code in an isolated namespace
    with the DataFrame injected as ``df``, captures matplotlib figure state,
    and returns pass/fail based on the assertion.

    Usage::

        import pandas as pd

        mock_df = pd.DataFrame({
            'year': [2016, 2017, 2018],
            'total_investment': [1_200_000_000, 2_500_000_000, 3_100_000_000],
        })

        def my_assertion(code: str, namespace: dict) -> bool:
            fig = namespace['__fig__']
            ax = fig.axes[0]
            assert ax.get_title() == 'Total Investments by Year'
            return True

        metric = ResolutionRateMetric()
        passed: bool = metric.evaluate(
            code="import matplotlib.pyplot as plt\nplt.bar(df['year'], df['total_investment'])",
            assertion=my_assertion,
            df=mock_df,
        )
    """

    def evaluate(
        self,
        code: str,
        assertion: Callable[[str, dict], bool],
        df: pd.DataFrame | None = None,
    ) -> bool:
        """Return True if the code passes the assertion.

        Args:
            code: Python code string to execute.
            assertion: Callable(code, namespace) -> bool. AssertionError
                       is caught and treated as False.
            df: DataFrame injected as ``df`` in the execution namespace.
        """
        if not code or not code.strip():
            logger.warning("ResolutionRateMetric: empty code string.")
            return False

        namespace = self._execute_code(code, df)
        return _safe_assert(assertion, code, namespace)

    def _execute_code(self, code: str, df: pd.DataFrame | None) -> dict:
        """Execute code in an isolated namespace with matplotlib Agg backend.

        Sets matplotlib to the non-interactive Agg backend, clears existing
        figures, execs the code with ``df`` injected into the namespace, and
        captures ``plt.gcf()`` into ``namespace['__fig__']`` after execution.
        Returns the namespace regardless of whether execution raised.
        """
        import matplotlib
        import matplotlib.pyplot as plt

        matplotlib.use("Agg")
        plt.close("all")

        namespace: dict = {"plt": plt}
        if df is not None:
            namespace["df"] = df

        try:
            exec(code, namespace)  # noqa: S102
        except Exception as e:
            logger.warning(f"ResolutionRateMetric: code execution raised: {e}")

        namespace["__fig__"] = plt.gcf()
        return namespace
