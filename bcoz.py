from argparse import Namespace, ArgumentParser


class Trad:
    def __init__(self):
        self.silent: bool = False
        self.args: Namespace = self.parse_arguments()

    def parse_arguments(self) -> Namespace:
        parser = ArgumentParser(description=
                                'A Python library with implementation of algorithms '
                                'for performing causal discovery.')
        parser.add_argument('-a', '--algorithm', action='store', type=str, required=True,
                            help='choose which algorithm to use',
                            choices=['bpc', 'eb', 'fas', 'fask', 'fask-concatenated', 'fci', 'fges', 'fges-mb',
                                     'fofc', 'ftfc', 'gfci', 'glasso', 'imgs_cont', 'imgs_disc', 'lingam', 'mbfs',
                                     'mgm', 'mimbuild', 'multi-fask', 'pc-all', 'r-skew', 'r-skew-e', 'r1', 'r2',
                                     'r3', 'r4', 'rfci', 'rfci-bsc', 'skew', 'skew-e', 'ts-fci', 'ts-gfci', 'ts-imgs'])
        parser.add_argument('-t', '--data_type', action='store', type=str, required=True,
                            help='tell me which data type the input data is',
                            choices=['continuous', 'covariance', 'discrete', 'mixed'])
        parser.add_argument('-d', '--dataset', action='store', type=str, required=True, nargs='+',
                            help='dataset file path. Multiple files are separated by commas.')
        parser.add_argument('--delimiter', action='store', type=str, default="comma",
                            help='Delimiter: colon, comma, pipe, semicolon, space, tab, whitespace',
                            choices=['colon', 'comma', 'pipe', 'semicolon', 'space', 'tab', 'whitespace'])
        parser.add_argument('-o', '--out', action='store', type=str, help='Output directory')
        parser.add_argument('--prefix', action='store', type=str, help='Output file name prefix')
        parser.add_argument('--thread', action='store', type=int, help='Number threads')
        parser.add_argument('--depth', action='store', type=int, default=-1, help='')
        parser.add_argument('--significance', action='store', type=float, default=0.05, help='')
        parser.add_argument('--seed', action='store', type=int, help='')
        parser.add_argument('--num_nodes', action='store', type=int, default=5, help='')
        parser.add_argument('--num_edges', action='store', type=int, default=5, help='')
        parser.add_argument('--knowledge', action='store', type=str, help='')
        parser.add_argument('--graphxml', action='store', type=str, help='')
        parser.add_argument('--graphtxt', action='store', type=str, help='')
        parser.add_argument('--initialgraphtxt', action='store', type=str, help='')
        parser.add_argument('--covariance', action="store_true", help='')
        parser.add_argument('--json_graph', action="store_true", help='Write out graph as json.')
        parser.add_argument('--skip_validation', action="store_true", help='Skip validation')
        parser.add_argument('--whitespace', action="store_true", help='')
        parser.add_argument('--sample_prior', action='store', type=float, default=1.0, help='')
        parser.add_argument('--structure_prior', action='store', type=float, default=1.0, help='')
        parser.add_argument('--penalty_discount', action='store', type=float, default=1.0, help='')
        parser.add_argument('--rfci', action="store_true", help='')
        parser.add_argument('--nodsep', action="store_true", help='')
        parser.add_argument('--silent', action="store_true", help='')
        parser.add_argument('--condcorr', action="store_true", help='')
        parser.add_argument('--verbose', action="store_true", help='')
        args = parser.parse_args()
        self.silent = args.silent
        return args

    def out_print(self, x: str):
        if not self.silent:
            print(x)

    def load_data(self):
        if not self.args.dataset:
            raise AttributeError("No data file was specified.")
        if not self.args.data_type:
            raise AttributeError("No data type (continuous/discrete) was specified.")
        self.out_print(f"Loading data from {self.args.dataset}.\n")
        # TODO load data

    def load_knowledge(self):
        if not self.args.knowledge:
            raise AttributeError("No knowledge file was specified.")
        # TODO load knowledge

    def run_algorithm(self):
        if not self.args.dataset:
            self.load_data()
        if not self.args.knowledge:
            self.load_knowledge()
        algorithm = self.args.algorithm
        if "pc" == algorithm:
            runPc()
        elif "fci" == algorithm:
            runFci()
        elif "fges" == algorithm:
            runFges()
        elif "fang" == algorithm:
            runFang()
        elif "pc.stable" == algorithm:
            runPcStable()
        elif "cpc" == algorithm:
            runCpc()
        elif "cfci" == algorithm:
            runCfci()
        elif "ccd" == algorithm:
            runCcd()
        elif "bayes_est" == algorithm:
            runBayesEst()
        elif "fofc" == algorithm:
            runFofc()
        elif "randomDag" == algorithm:
            printRandomDag()
        else:
            TetradLogger.getInstance().reset()
            TetradLogger.getInstance().removeOutputStream(System.out)
            raise AttributeError("No algorithm was specified.")


def main():
    trad = Trad()
    trad.run_algorithm()


if __name__ == '__main__':
    main()
