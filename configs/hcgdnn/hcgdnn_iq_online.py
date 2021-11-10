_base_ = '../_base_/default_runtime.py'

dataset_type = 'WTIMCOnlineDataset'
data_root = '/home/citybuster/Data/SignalProcessing/ModulationClassification/online'
data = dict(
    samples_per_gpu=160,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='train.json',
        channel_mode=True,
        merge_res=True,
        use_cache=True,
    ),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='val.json',
        channel_mode=True,
        merge_res=True,
        use_cache=True,
    ),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='val.json',
        channel_mode=True,
        merge_res=True,
        use_cache=True,
    ),
)

in_size = 100
out_size = 288
# Model
model = dict(
    type='HCGDNN',
    backbone=dict(
        type='HCGNetV2',
        input_size=in_size,
    ),
    classifier_head=dict(
        type='ABLHAMCHead',
        in_features=in_size,
        out_features=out_size,
        num_classes=5,
        loss_cls=dict(
            type='CrossEntropyLoss',
            loss_weight=1,
        ),
    ),
)

train_cfg = dict()
test_cfg = dict()

total_epochs = 1600

# Optimizer
optimizer = dict(type='Adam', lr=0.00001)
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(
    policy='step',
    gamma=0.3,
    step=[800])
