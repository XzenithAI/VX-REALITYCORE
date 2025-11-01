"""
VX Domains - Domain-Specific Intelligence Adapters

Domains allow VX to specialize for different contexts:
- DAO governance
- Policy analysis
- Health monitoring
- Personal assistance
- Research
- Creative work

Each domain provides:
- Specialized input processors
- Domain-specific actions
- Custom evaluation metrics
- Adapted scroll laws

Author: Flame Architect
Seal: VX-FLAMESEAL-2025-DOMAINS
"""

from .base_domain import BaseDomain
from .general_domain import GeneralDomain
from .dao_domain import DAODomain

__all__ = [
    'BaseDomain',
    'GeneralDomain',
    'DAODomain'
]

__version__ = '1.0.0-IGNITION'
