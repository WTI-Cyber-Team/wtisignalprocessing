_base_ = '../_base_/default_runtime.py'

# Dataset
dataset_type = 'SlotDataset'
data_root = '/home/zry/Data/SignalProcessing/ModulationClassification/MATSLOT/Con_128_Ds150_36000'
data = dict(
    samples_per_gpu=40,
    workers_per_gpu=1,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='train.json',
    ),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='test.json',
    ),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='test.json',
    ),
)

# Model
model = dict(
    type='SCDN',
    backbone=dict(
        type='ScdnNet',
        slot_size=128,
    ),
    classifier_head=dict(
        type='DSAMCHead',
        num_classes=8,
        in_features=64,
        loss_cls=dict(
            type='CrossEntropyLoss',
            loss_weight=1.0,
        ),
    ),
)

train_cfg = dict()
test_cfg = dict()

total_epochs = 100

# Optimizer
optimizer = dict(type='RMSprop', lr=0.001, alpha=0.9, eps=1e-07)
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(policy='fixed')
