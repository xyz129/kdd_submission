from pathlib import Path

from numpy import log
from pandas import read_csv

from algorithms.Tree.utils import get_num_cols
from experiments.config_object import Config
from experiments.default_config import GBM_REGRESSORS, GBM_CLASSIFIERS, N_EXPERIMENTS, SEED, KFOLDS
from experiments.experiment_configurator import experiment_configurator
from experiments.preprocess_pipelines import get_preprocessing_pipeline_only_cat, get_preprocessing_pipeline

EXP = "kaggle_hp"


def get_x_y(apply_log=True):
    project_root = Path(__file__).parent.parent.parent.parent
    y_col_name = 'SalePrice'
    train = read_csv(project_root / 'datasets/house_prices_kaggle/train.csv')
    y = train[y_col_name]
    X = train.drop(columns=[y_col_name, "Id"])
    for col in X.select_dtypes('O').columns:
        X[col] = X[col].astype('category')
    if apply_log:
        y = log(train[y_col_name])
    return X, y


if __name__ == '__main__':
    MULTIPLE_EXPERIMENTS = False
    KFOLD = True
    ONE_HOT = False
    COMPUTE_PERMUTATION = False
    RESULTS_DIR = Path("speed_test/") # Path(F"{EXP}no_id_Log/")

    x, y = get_x_y()
    regression = not (len(y.value_counts()) == 2)
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
