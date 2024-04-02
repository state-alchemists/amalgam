from zrb import BoolInput

enable_monitoring_input = BoolInput(
    name="enable-myapp-monitoring",
    description='Enable "myapp" monitoring',
    prompt='Enable "myapp" monitoring?',
    default=False,
)
