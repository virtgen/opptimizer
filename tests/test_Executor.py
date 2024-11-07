from opptimizer.Executor import Executor


def test_run():

    executor = op.Executor(modules = ['pass',op.Mod(exec_func, "abak2")])
    test = executor.run(context = op.opp('dataloop',1),cfg = 'opp_run.cfg', scope = (op.opprange('sampleParam', 0,1)))

    executor 
    assert result == 5  # Expected outcome