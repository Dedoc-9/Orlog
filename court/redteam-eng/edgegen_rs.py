"""Every 7th program of the edge battery (for the Rust backend run)."""
import edgegen


def generate(seed):
    return edgegen.generate(seed * 7)
