from graph.Graph import Graph


class TimeLagGraph(Graph):
    """
    Represents a time series graph--that is, a graph with a fixed number S of lags,
    with edges into initial lags only--that is, into nodes in the first R lags, for some R.
    Edge structure repeats every R nodes.
    """
