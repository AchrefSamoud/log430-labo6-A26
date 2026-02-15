"""
Saga states
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from enum import Enum

# TODO: Veuillez consulter le diagramme de machine à états pour en savoir plus
class OrderSagaState(Enum):
    START = 0
    ORDER_CREATED = 1
    STOCK_DECREASED = 2
    PAYMENT_CREATED = 3
    STOCK_INCREASED = 4
    ORDER_DELETED = 5
    END = 6
