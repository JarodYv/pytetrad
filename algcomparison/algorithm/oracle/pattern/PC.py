from typing import List

from algcomparison.algorithm.Algorithm import Algorithm
from algcomparison.utils.HasKnowledge import HasKnowledge
from algcomparison.utils.TakesInitialGraph import TakesInitialGraph
from algcomparison.utils.TakesIndependenceWrapper import TakesIndependenceWrapper
from algcomparison.independence.IndependenceWrapper import IndependenceWrapper
from data.DataModel import DataModel
from data.DataType import DataType
from graph.Graph import Graph
from data.Knowledge import Knowledge
from util import Parameters
from search.SearchGraphUtils import SearchGraphUtils
from graph.EdgeListGraph import EdgeListGraph
from search.PcAll import PcAll, FasType, ColliderDiscovery, Concurrent
from search.ConflictRule import ConflictRule


class PC(Algorithm, TakesInitialGraph, HasKnowledge, TakesIndependenceWrapper):
    """
    PC
    """

    def __init__(self, test: IndependenceWrapper = None, algorithm: Algorithm = None):
        self.test = test
        self.algorithm = algorithm
        self.initial_graph: Graph = None
        self.knowledge: Knowledge = None

    def search(self, dataset: DataModel, **parameters) -> Graph:
        # if parameters["number_resampling"] < 1:
        search = PcAll(self.test.get_test(dataset, **parameters), self.initial_graph)
        search.set_depth(parameters.get("depth"))
        search.set_knowledge(self.knowledge)
        search.set_conflict_rule(ConflictRule.PRIORITY)
        search.set_verbose(parameters.get("verbose"))
        search.set_collider_discovery(ColliderDiscovery.FAS_SEPSETS)
        search.set_fas_type(FasType.REGULAR)
        search.set_concurrent(Concurrent.NO)
        return search.search()

        # else:
        #     algorithm = Pc(self.test)
        #     data = dataset
        #     search = GeneralResamplingTest(data, algorithm, parameters.get("number_resampling"))
        #     search.set_knowledge(self.knowledge)
        #     search.setPercentResampleSize(parameters.get("percentResampleSize"))
        #     search.setResamplingWithReplacement(parameters.get("resamplingWithReplacement"))
        #     edge_ensemble = parameters.get("resamplingEnsemble", 1)
        #     if edge_ensemble == 0:
        #         edge_ensemble = ResamplingEdgeEnsemble.Preserved
        #     elif edge_ensemble == 1:
        #         edge_ensemble = ResamplingEdgeEnsemble.Highest
        #     elif edge_ensemble == 2:
        #         edge_ensemble = ResamplingEdgeEnsemble.Majority
        #     else:
        #         edge_ensemble = ResamplingEdgeEnsemble.Highest
        #     search.setEdgeEnsemble(edge_ensemble)
        #     search.setAddOriginalDataset(parameters.get("addOriginalDataset"))
        #     search.set_verbose(parameters.get("verbose"))
        #     search.setParameters(**parameters)
        #     return search.search()

    def get_comparison_graph(self, graph: Graph) -> Graph:
        return SearchGraphUtils.pattern_for_dag(EdgeListGraph(graph, nodes=None))

    def get_description(self) -> str:
        independence_desc = "no independence test" if not self.test else self.test.get_description()
        algorithm_desc = "" if not self.algorithm else f" with initial graph from {self.algorithm.get_description()}"
        return f"PC (\"Peter & Clark\"), Priority Rule, using {independence_desc} {algorithm_desc}"

    def get_data_type(self) -> DataType:
        return self.test.get_data_type()

    def get_parameters(self) -> List[str]:
        parameters = ["depth", "verbose"]
        return parameters

    def get_initial_graph(self) -> Graph:
        return self.initial_graph

    def set_initial_graph(self, graph: Graph):
        self.initial_graph = graph

    def set_initial_graph_from_algorithm(self, algorithm: Algorithm):
        self.algorithm = algorithm

    def get_knowledge(self) -> Knowledge:
        return self.knowledge

    def set_knowledge(self, knowledge: Knowledge):
        self.knowledge = knowledge

    def set_independence_wrapper(self, wrapper: IndependenceWrapper):
        self.test = wrapper

    def get_independence_wrapper(self) -> IndependenceWrapper:
        return self.test