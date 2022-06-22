import random
import sys
import torch
import argparse
import yaml
import numpy as np

from easydict import EasyDict as edict
from cv.supernet_transformer import Vision_TransformerSuper
from search.SearchEngineFactory import SearchEngineFactory
from search.utils import Timer, parse_config

def parse_args(args):
    parser = argparse.ArgumentParser('DE-NAS')
    parser.add_argument('--domain', type=str, default=None, choices=['cnn','vit'], help='DE-NAS search domain')
    parser.add_argument('--conf', type=str, default=None, help='DE-NAS conf file')
    input_args = edict(parser.parse_args(args).__dict__)
    settings = {}
    settings.update(input_args)
    settings.update(parse_config(input_args.conf))
    return edict(settings)

def main(params):

    if params.domain == 'cnn':
        from cv.third_party.ZenNet import DeSearchSpaceXXBL as search_space
        from cv.third_party.ZenNet import DeMainNet as super_net
    elif params.domain == 'vit':
        # set ViT seed for reproducibility
        torch.manual_seed(params.seed)
        np.random.seed(params.seed)
        random.seed(params.seed)
        with open(params.supernet_cfg) as f:
            cfg = edict(yaml.safe_load(f))
        super_net = Vision_TransformerSuper(img_size=params.img_size,
                                    patch_size=params.patch_size,
                                    embed_dim=cfg.SUPERNET.EMBED_DIM, depth=cfg.SUPERNET.DEPTH,
                                    num_heads=cfg.SUPERNET.NUM_HEADS,mlp_ratio=cfg.SUPERNET.MLP_RATIO,
                                    qkv_bias=True, drop_rate=params.drop_rate,
                                    drop_path_rate=params.drop_path_rate,
                                    gp=params.gp,
                                    num_classes=10,
                                    max_relative_position=params.max_relative_position,
                                    relative_position=params.relative_position,
                                    change_qkv=params.change_qkv, abs_pos=params.abs_pos)
        search_space = {'num_heads': cfg.SEARCH_SPACE.NUM_HEADS, 'mlp_ratio': cfg.SEARCH_SPACE.MLP_RATIO,
                        'embed_dim': cfg.SEARCH_SPACE.EMBED_DIM , 'depth': cfg.SEARCH_SPACE.DEPTH}

    '''
    Unified Call for DE-NAS Search Engine
    -------
    Parameters: params, super_net, search_space
    '''
    with Timer("DE-NAS search best structure"):
        searcher = SearchEngineFactory.create_search_engine(params = params, super_net = super_net, search_space = search_space)
        searcher.search()
    best_structure = searcher.get_best_structures()
    print(f"DE-NAS completed, best structure is {best_structure}")

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main(args)