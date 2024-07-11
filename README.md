# `mainframe`

Project Structure

```md
mainframe/
│
├── mainframe/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config_manager.py
│   │   ├── task_scheduler.py
│   │   ├── resource_manager.py
│   │   └── exceptions.py
│   ├── kernels/
│   │   ├── __init__.py
│   │   ├── base_kernel.py
│   │   ├── fiji/
│   │   │   ├── __init__.py
│   │   │   ├── fiji_kernel.py
│   │   │   └── fiji_instance.py
│   │   └── os/
│   │       ├── __init__.py
│   │       └── os_utils.py
│   └── utils/
│       ├── __init__.py
│       └── common_utils.py
│
├── configs/
│   └── routine.json
│
├── tests/
│   ├── __init__.py
│   ├── test_config_manager.py
│   ├── test_task_scheduler.py
│   ├── test_resource_manager.py
│   └── test_fiji_kernel.py
│
├── examples/
│   └── example_usage.py
│
├── docs/
│   ├── README.md
│   └── CONTRIBUTING.md
│
├── setup.py
├── requirements.txt
├── .gitignore
└── LICENSE
```

