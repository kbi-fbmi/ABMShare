"""Initialize Covasim by importing all the modules

Convention is to use "import covasim as cv", and then to use all functions and
classes directly, e.g. cv.Sim() rather than cv.sim.Sim().
"""

# Check that requirements are met and set options
from . import requirements
from .analysis import *  # Depends on utils, misc, interventions
from .base import *  # Depends on version, misc, defaults, parameters, utils

# Import the actual model
from .defaults import *  # Depends on settings
from .immunity import *  # Depends on utils, parameters, defaults
from .interventions import *  # Depends on defaults, utils, base
from .misc import *  # Depends on version
from .parameters import *  # Depends on settings, misc
from .people import *  # Depends on utils, defaults, base, plotting
from .plotting import *  # Depends on defaults, misc
from .population import *  # Depends on people et al.
from .run import *  # Depends on sim
from .settings import *
from .sim import *  # Depends on almost everything
from .utils import *  # Depends on defaults

# Import the version and print the license unless verbosity is disabled, via e.g. os.environ['COVASIM_VERBOSE'] = 0
from .version import __license__, __version__, __versiondate__


