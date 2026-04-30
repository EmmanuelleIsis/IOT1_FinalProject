# src/state_machine.py

def compute_state(water_level, W_warn=5.0, W_crit=10.0):
    if water_level is None:
        return "NORMAL"  # fallback

    if water_level < W_warn:
        return "NORMAL"
    elif water_level < W_crit:
        return "WARNING"
    else:
        return "FLOOD_RISK"
