"""Check that correct versions of each library are installed, and print warnings
or errors if not.
"""

#%% Housekeeping

__all__ = ["min_versions", "check_sciris", "check_synthpops"]

min_versions = {"sciris":"1.3.3"} # Should match requirements.txt


#%% Check dependencies

def check_sciris():
    """Check that Sciris is available and the right version"""
    try:
        import sciris as sc
    except ModuleNotFoundError: # pragma: no cover
        errormsg = 'Sciris is a required dependency but is not found; please install via "pip install sciris==2.1.0"'
        raise ModuleNotFoundError(errormsg)
    ver = sc.__version__
    minver = min_versions["sciris"]
    if sc.compareversions(ver, minver) < 0:
        errormsg = f'You have Sciris {ver} but {minver} is required; please upgrade via "pip install --upgrade sciris"'
        raise ImportError(errormsg)
    return


def check_synthpops(verbose=False, die=False):
    """Check whether synthpops is available"""
    # Check synthpops -- optional dependency
    try:
        import synthpops
        return synthpops
    except ModuleNotFoundError as E: # pragma: no cover
        import_error = f"Synthpops (for detailed demographic data) is not available ({str(E)})\n"
        if die:
            raise ModuleNotFoundError(import_error)
        if verbose:
            print(import_error)
        return False

    return None

# Perform the version checks on import
check_sciris()
