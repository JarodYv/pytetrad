from typing import List, Optional

from algcomparison.algorithm.Algorithm import Algorithm
from algcomparison.utils.HasKnowledge import HasKnowledge
from algcomparison.utils.TakesInitialGraph import TakesInitialGraph
from algcomparison.utils.TakesIndependenceWrapper import TakesIndependenceWrapper
from algcomparison.independence.IndependenceWrapper import IndependenceWrapper
from data.DataModel import DataModel
from data.DataType import DataType
from graph.Graph import Graph
from data.Knowledge import Knowledge
from search.SearchGraphUtils import SearchGraphUtils
from graph.EdgeListGraph import EdgeListGraph
from search.PcAll import PcAll, FasType, ColliderDiscovery, Concurrent
from search.ConflictRule import ConflictRule


class CPC(Algorithm, TakesInitialGraph, HasKnowledge, TakesIndependenceWrapper):
    """
    CPC
    """

    def __init__(self, test: Optional[IndependenceWrapper] = None, algorithm: Optional[Algorithm] = None):
        self.test = test
        self.algorithm = algorithm
        self.initial_graph: Optional[Graph] = None
        self.knowledge: Optional[Knowledge] = None

    def search(self, dataset: DataModel, **parameters) -> Graph:
        # if parameters["number_resampling"] < 1:
        collider_discovery: ColliderDiscovery = parameters.get("collider_discovery_rule", ColliderDiscovery.FAS_SEPSETS)
        conflict_rule: ConflictRule = parameters.get("conflict_rule", ConflictRule.OVERWRITE)

        search = PcAll(self.test.get_test(dataset, **parameters), self.initial_graph)
        search.set_depth(parameters.get("depth"))
        search.set_heuristic(parameters.get("fas_heuristic", 0))
        search.set_knowledge(self.knowledge)
        if parameters.get("stable_FAS", False):
            search.set_fas_type(FasType.STABLE)
        else:
            search.set_fas_type(FasType.REGULAR)
        if parameters.get("concurrent_FAS", False):
            search.set_concurrent(Concurrent.YES)
        else:
            search.set_concurrent(Concurrent.NO)
        search.set_collider_discovery(collider_discovery)
        search.set_conflict_rule(conflict_rule)
        search.set_use_heuristic(parameters.get("use_max_p_orientation_heuristic", False))
        search.set_max_path_length(parameters.get("max_p_orientation_max_path_length", 0))
        search.set_verbose(parameters.get("verbose"))

        return search.search()

        # else:
        #     algorithm = Pc(self.test, self.algorithm)
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
        algorithm_desc = "" if not self.algorithm else f"with initial graph from {self.algorithm.get_description()}"
        return f"PC using {independence_desc} {algorithm_desc}"

    def get_data_type(self) -> DataType:
        return self.test.get_data_type()

    def get_parameters(self) -> List[str]:
        parameters = ["depth", "stable_FAS", "concurrent_FAS", "collider_discovery_rule", "collider_discovery_rule",
                      "conflict_rule", "fas_heuristic", "use_max_p_orientation_heuristic",
                      "max_p_orientation_max_path_length", "verbose"]
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
