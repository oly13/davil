"""
    Clustering controller
"""
import logging
import pandas as pd
from ....backend.algorithms.clustering.clustering_register import ClusteringRegister
from ....backend.algorithms.clustering.dummy_clustering import DUMMY_ID
from .abstract_algorithm_controller import AbstractAlgorithmController

class ClusterController(AbstractAlgorithmController):
    """Controls the clustering of the values for the values dataframe"""
    LOGGER = logging.getLogger(__name__)
    CLUSTERING_COLOR_COLUMN = 'color'
    DEFAULT_LABEL_COLORS = ["red", "navy", "green", "orange", "grey", "yellow", "black"]

    def __init__(self, algorithm_id=None, source=None, label_colors=None, n_clusters=4):
        algorithm_dict = ClusteringRegister.get_algorithm_dict()
        super(ClusterController, self).\
              __init__(DUMMY_ID,
                       algorithm_dict,
                       active_algorithm_id=algorithm_id)
        self._clustering_dic = dict()
        self._label_colors = label_colors
        if not self._label_colors:
            self._label_colors = ClusterController.DEFAULT_LABEL_COLORS
        self._source = source
        self._n_clusters = n_clusters

    def update_clusters(self, dimension_values_df):
        """dimension_values_df: (pandas.Dataframe) values of the points
        """
        algorithm_id = self.get_active_algorithm_id()
        labels = None
        pair_key = (algorithm_id, self._n_clusters)
        if pair_key in self._clustering_dic:
            labels = self._clustering_dic[pair_key]
        else:
            labels = self.execute_active_algorithm(dimension_values_df,
                                                   n_clusters=self._n_clusters)
            self._clustering_dic[pair_key] = labels

        colors = [self._label_colors[i] for i in labels]
        if self._source:
            self._source.data['color'] \
                = pd.Series(colors, index=dimension_values_df.index)

    def update_number_of_clusters(self, n_clusters):
        if n_clusters < 3:
            raise ValueError('The number of clusters must be greater than 2.\
                             Received {}'.format(n_clusters))
        self._n_clusters = n_clusters        

    def get_number_of_clusters(self):
        return self._n_clusters

    def get_classes(self):
        pair_key = (self.get_active_algorithm_id(), self._n_clusters)
        labels = self._clustering_dic[pair_key]
        return labels