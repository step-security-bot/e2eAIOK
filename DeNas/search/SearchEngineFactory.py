from search.RandomSearchEngine import RandomSearchEngine
from search.EvolutionarySearchEngine import EvolutionarySearchEngine
from search.CNNRandomSearchEngine import CNNRandomSearchEngine

SEARCHER_TYPES = {
        "RandomSearchEngine": RandomSearchEngine,
        "EvolutionarySearchEngine": EvolutionarySearchEngine,
        "CNNRandomSearchEngine": CNNRandomSearchEngine
}

class SearchEngineFactory(object):

    @staticmethod
    def create_search_engine(params, super_net, search_space):
        try:
            return SEARCHER_TYPES[params.search_engine](params, super_net, search_space)
        except Exception:
            return None