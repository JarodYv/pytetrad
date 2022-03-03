from typing import List, Optional

from algcomparison.algorithm.Algorithm import Algorithm
from algcomparison.independence.IndependenceWrapper import IndependenceWrapper
from algcomparison.utils.HasKnowledge import HasKnowledge
from algcomparison.utils.TakesIndependenceWrapper import TakesIndependenceWrapper
from algcomparison.utils.TakesInitialGraph import TakesInitialGraph
from data.DataModel import DataModel
from data.DataType import DataType
from data.Knowledge import Knowledge
from graph.EdgeListGraph import EdgeListGraph
from graph.Graph import Graph
from search.ConflictRule import ConflictRule
from search.PcAll import ColliderDiscovery, PcAll, FasType, Concurrent
from search.SearchGraphUtils import SearchGraphUtils


class PCAll(Algorithm, TakesInitialGraph, HasKnowledge, TakesIndependenceWrapper):
    def __init__(self, test: Optional[IndependenceWrapper] = None, algorithm: Optional[Algorithm] = None):
        self.test = test
        self.algorithm = algorithm
        self.initial_graph: Graph | None = None
        self.knowledge: Knowledge | None = None

    def get_comparison_graph(self, graph: Graph) -> Graph:
        return SearchGraphUtils.pattern_for_dag(EdgeListGraph(graph, nodes=None))

    def get_description(self) -> str:
        independence_desc = self.test.get_description() if self.test else "no independence test"
        algorithm_desc = f" with initial graph from {self.algorithm.get_description()}" if self.algorithm else ""
        return "PC using " + independence_desc + algorithm_desc

    def get_data_type(self) -> DataType:
        return self.test.get_data_type()

    def get_parameters(self) -> List[str]:
        parameters = ["stableFAS", "concurrentFAS", "colliderDiscoveryRule", "conflictRule", "depth", "fasHeuristic",
                      "useMaxPOrientationHeuristic", "maxPOrientationMaxPathLength", "verbose"]
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

    def search(self, dataset: DataModel, **parameters) -> Graph:
        if parameters.get("numberResampling", 0) < 1:
            collider_discovery_rule = parameters.get("colliderDiscoveryRule", 0)
            if collider_discovery_rule == 1:
                collider_discovery = ColliderDiscovery.FAS_SEPSETS
            elif collider_discovery_rule == 2:
                collider_discovery = ColliderDiscovery.CONSERVATIVE
            elif collider_discovery_rule == 3:
                collider_discovery = ColliderDiscovery.MAX_P
            else:
                raise ValueError("colliderDiscoveryRule should in [1, 2, 3]")

            rule = parameters.get("conflictRule", 0)
            if rule == 1:
                conflict_rule = ConflictRule.OVERWRITE
            elif rule == 2:
                conflict_rule = ConflictRule.BIDIRECTED
            elif rule == 3:
                conflict_rule = ConflictRule.PRIORITY
            else:
                raise ValueError("conflictRule should in [1, 2, 3]")

            search = PcAll(self.test.get_test(dataset, **parameters), self.initial_graph)
            search.set_depth(parameters.get("depth"))
            search.set_heuristic(parameters.get("fasHeuristic"))
            search.set_knowledge(self.knowledge)

            if parameters.get("stableFAS", False):
                search.set_fas_type(FasType.STABLE)
            else:
                search.set_fas_type(FasType.REGULAR)

            if parameters.get("concurrentFAS", False):
                search.set_concurrent(Concurrent.YES)
            else:
                search.set_concurrent(Concurrent.NO)

            search.set_collider_discovery(collider_discovery)
            search.set_conflict_rule(conflict_rule)
            search.set_use_heuristic(parameters.get("useMaxPOrientationHeuristic", False))
            search.set_max_path_length(parameters.get("maxPOrientationMaxPathLength", 0))
            search.set_verbose(parameters.getBoolean("verbose", False))

            return search.search()
        else:
            raise ValueError("have not implement resampling algorithm")
            # pcAll = PCAll(self.test, self.algorithm)
            # if self.initial_graph:
            #     pcAll.set_initial_graph(self.initial_graph)
            # search = GeneralResamplingTest(dataset, pcAll, parameters.get("numberResampling", 0))
            # search.set_knowledge(self.knowledge)
            #
            # search.setPercentResampleSize(parameters.get("percentResampleSize", 1.0))
            # search.setResamplingWithReplacement(parameters.get("resamplingWithReplacement", False))
            #
            # edge_ensemble = ResamplingEdgeEnsemble.Highest
            # resampling_ensemble = parameters.get("resamplingEnsemble", 1)
            # if resampling_ensemble == 0:
            #     edge_ensemble = ResamplingEdgeEnsemble.Preserved
            # elif resampling_ensemble == 1:
            #     edge_ensemble = ResamplingEdgeEnsemble.Highest
            # elif resampling_ensemble == 2:
            #     edge_ensemble = ResamplingEdgeEnsemble.Majority
            #
            # search.setEdgeEnsemble(edge_ensemble)
            # search.setAddOriginalDataset(parameters.get("addOriginalDataset", False))
            #
            # search.setParameters(**parameters)
            # search.setVerbose(parameters.getBoolean("verbose", False))
            # return search.search()
