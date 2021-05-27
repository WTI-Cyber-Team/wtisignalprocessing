import torch.nn as nn

from .location import BaseLocation
from ..builder import TASKS, build_backbone, build_head
from ...common.utils import outs2result


@TASKS.register_module()
class RILCLDNN(BaseLocation):

    def __init__(self, backbone, classifier_head, train_cfg=None, test_cfg=None):
        super(RILCLDNN, self).__init__()
        self.backbone = build_backbone(backbone)
        self.classifier_head = build_head(classifier_head)
        self.train_cfg = train_cfg
        self.test_cfg = test_cfg
        self.softmax = nn.Softmax(dim=1)

        # init weights
        self.init_weights()

    def init_weights(self, pre_trained=None):
        """Initialize the weights in task.

        Args:
            pre_trained (str, optional): Path to pre-trained weights.
                Defaults to None.
        """
        super(RILCLDNN, self).init_weights(pre_trained)
        self.backbone.init_weights(pre_trained=pre_trained)

        self.classifier_head.init_weights()

    def extract_feat(self, x):
        """Directly extract features from the backbone."""
        x = self.backbone(x)
        return x

    def forward_train(self, x, px, py):
        x = self.extract_feat(x)
        losses = self.classifier_head.forward_train(
            x, px=px, py=py)

        return losses

    def simple_test(self, x):
        x = self.extract_feat(x)
        outs = self.classifier_head(x)

        tmp_outs = dict()
        for key_str in outs.keys():
            if 'x' in key_str:
                tmp_key = 'px'
            else:
                tmp_key = 'py'
            tmp_outs[tmp_key] = self.softmax(outs[key_str])

        outs = tmp_outs

        results_list = []
        keys = list(outs.keys())
        batch_size = outs[keys[0]].shape[0]
        for idx in range(batch_size):
            item = dict()
            for key_str in keys:
                item[key_str] = outs2result(outs[key_str][idx, :])
            results_list.append(item)

        return results_list