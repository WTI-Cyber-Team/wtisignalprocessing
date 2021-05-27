_base_ = '../_base_/default_runtime.py'

dataset_type = 'WTIMCDataset'
data_root = '/home/citybuster/Data/SignalProcessing/ModulationClassification/DeepSig/201610A'
data = dict(
    samples_per_gpu=80,
    workers_per_gpu=1,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='train_and_val.json',
        iq=True,
        ap=False,
    ),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='test.json',
        iq=True,
        ap=False,
    ),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='test.json',
        iq=True,
        ap=False,
    ),
)

model = dict(
    type='CRNN',
    is_iq=True,
    backbone=dict(
        type='MLNetV7',
        dropout_rate=0.5,
    ),
    classifier_head=dict(
        type='AMCHead',
        num_classes=11,
        in_features=100,
        out_features=256,
        loss_cls=dict(
            type='CrossEntropyLoss',
            loss_weight=1,
        )
    ),
)
train_cfg = dict()
test_cfg = dict()

total_epochs = 400
# optimizer
optimizer = dict(type='Adam', lr=0.0004)
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(policy='fixed')
