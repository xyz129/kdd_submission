from pathlib import Path

from pandas import read_csv

from algorithms.Tree.utils import get_num_cols
from experiments.config_object import Config
from experiments.default_config import GBM_CLASSIFIERS
from experiments.default_config import GBM_REGRESSORS, N_EXPERIMENTS, SEED, KFOLDS
from experiments.experiment_configurator import experiment_configurator
from experiments.preprocess_pipelines import get_preprocessing_pipeline_only_cat, get_preprocessing_pipeline


def get_x_y():
    project_root = Path(__file__).parent.parent.parent.parent
    y_col_name = 'IsBadBuy'
    train = read_csv(project_root / 'datasets/dont_get_kicked_catboost/training.csv')
    y = train[y_col_name]
    X = train.drop(columns=[y_col_name])
    for col in train.select_dtypes(include=['O']).columns.tolist() + ['WheelTypeID', 'BYRNO','VNZIP1']:
        X[col] = X[col].astype('category')
    return X, y


if __name__ == '__main__':
    MULTIPLE_EXPERIMENTS = False
    KFOLD = True
    ONE_HOT = False
    COMPUTE_PERMUTATION = True
    RESULTS_DIR = Path("10Fold/")

    x, y = get_x_y()
    regression = not(len(y.value_counts()) == 2)
    contains_num_features = len(get_num_cols(x.dtypes)) > 0
    pp = get_preprocessing_pipeline if contains_num_features else get_preprocessing_pipeline_only_cat
    predictors = GBM_REGRESSORS if regression else GBM_CLASSIFIERS
    config = Config(
        multiple_experimens=MULTIPLE_EXPERIMENTS,
        n_experiments=N_EXPERIMENTS,
        kfold_flag=KFOLD,
        compute_permutation=COMPUTE_PERMUTATION,
        save_results=True,
        one_hot=ONE_HOT,
        contains_num_features=contains_num_features,
        seed=SEED,
        kfolds=KFOLDS,
        predictors=predictors,
        columns_to_remove=[],
        get_x_y=get_x_y,
        results_dir=RESULTS_DIR,
        preprocessing_pipeline=pp)
    experiment_configurator(config)

