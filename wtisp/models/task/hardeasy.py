import torch

from .amc import BaseAMC
from ..builder import TASKS, build_backbone, build_head
from ...common.utils import outs2result


@TASKS.register_module()
class HardEasy(BaseAMC):

    def __init__(self, backbone, classifier_head, train_cfg=None, test_cfg=None):
        super(HardEasy, self).__init__()
        self.backbone = build_backbone(backbone)
        self.classifier_head = build_head(classifier_head)
        self.train_cfg = train_cfg
        self.test_cfg = test_cfg

        # init weights
        self.init_weights()

    def init_weights(self, pre_trained=None):
        """Initialize the weights in task.

        Args:
            pre_trained (str, optional): Path to pre-trained weights.
                Defaults to None.
        """
        super(HardEasy, self).init_weights(pre_trained)
        self.backbone.init_weights(pre_trained=pre_trained)

        self.classifier_head.init_weights()

    def extract_feat(self, x):
        """Directly extract features from the backbone."""
        x = self.backbone(x)
        return x

    def forward_train(self, iqs, aps, cos, hard_labels, **kwargs):
        if iqs is None:
            x = aps
        elif aps is None:
            x = iqs
        else:
            x = torch.cat((iqs, aps), dim=1)
        x = self.extract_feat(x)
        losses = self.classifier_head.forward_train(x, mod_labels=hard_labels)

        return losses

    def simple_test(self, iqs, aps, cos):
        if iqs is None:
            x = aps
        elif aps is None:
            x = iqs
        else:
            x = torch.cat((iqs, aps), dim=1)
        x = self.extract_feat(x)
        outs = self.classifier_head(x)

        results_list = []
        for idx in range(outs.shape[0]):
            result = outs2result(outs[idx, :])
            results_list.append(dict(hard=result))

        return results_list
