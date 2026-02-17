"""
Handler: delete order
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import requests
from logger import Logger
from handlers.handler import Handler
from order_saga_state import OrderSagaState

class DeleteOrderHandler(Handler):
    """ Handle order deletion. """

    def __init__(self, order_id):
        """ Constructor method """
        self.order_id = order_id
        super().__init__()

    def run(self):
        """Call StoreManager to check out from stock"""
        # TODO: utilisez l'ID de la commande pour la supprimer (vous pouvez utiliser les autres handlers comme réference d'implementation)
        self.logger.debug(f"Transition d'état: DeleteOrder -> ORDER_DELETED")
        return OrderSagaState.ORDER_DELETED
        
    def rollback(self):
        """
        La transition d'état DeleteOrder est une compensation. Si la compensation échoue, notre implémentation passe simplement à l'état suivant jusqu'à atteindre l'état final (veuillez consulter le diagramme de machine à états pour en savoir plus). 
        Ainsi, nous n'utiliserons pas la méthode rollback() dans les handlers qui effectuent des rollbacks (comme cela). Toutefois, dans une implémentation plus robuste, nous pourrions réessayer le rollback en cas d'échec et ensuite passer au prochain état.
        Nous héritons de la classe abstraite Handler, et par conséquent, l'implémentation de la méthode rollback() est obligatoire.
        """
        pass
