from slam.utils.stopping_criterion import StoppingCriterion


def test_is_active():
    assert StoppingCriterion.is_active() is False
    StoppingCriterion.state.is_memory_limit = True
    assert StoppingCriterion.is_active() is True


def test_reset():
    StoppingCriterion.state.is_memory_limit = True
    StoppingCriterion.reset()
    assert StoppingCriterion.is_active() is False
