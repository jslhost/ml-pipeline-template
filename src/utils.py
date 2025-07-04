import yaml

def load_params(param_path: str = "params.yaml") -> dict:
    """Load parameters from a YAML file."""
    with open(param_path, "r") as f:
        params = yaml.safe_load(f)
    return params
