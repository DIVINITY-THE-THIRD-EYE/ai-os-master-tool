============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\PC\OneDrive\Documents\Master tool
configfile: pyproject.toml
plugins: anyio-4.14.2, cov-7.1.0
collected 63 items

tests\benchmark\test_agent_benchmark.py .                                [  1%]
tests\benchmark_v2\test_benchmark_v2.py .                                [  3%]
tests\chaos\test_corrupt_snapshot.py .                                   [  4%]
tests\chaos\test_persistence_chaos.py ..                                 [  7%]
tests\chaos\test_sigkill.py .                                            [  9%]
tests\compiler\test_prompt_compiler.py .                                 [ 11%]
tests\discovery\test_dynamic_discovery.py .                              [ 12%]
tests\distributed\test_distributed_evaluation.py .                       [ 14%]
tests\enforcement\test_budget_enforcement.py ....                        [ 20%]
tests\enforcement\test_quality_gates.py ..                               [ 23%]
tests\governance\test_governance.py ...                                  [ 28%]
tests\hybrid\test_hybrid_graph.py ..                                     [ 31%]
tests\observability\test_observability.py .                              [ 33%]
tools\test_runtime.py ..........................................         [100%]

======================= 63 passed in 903.54s (0:15:03) ========================
