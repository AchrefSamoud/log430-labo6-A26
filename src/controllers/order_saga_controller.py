"""
Order saga controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from handlers.create_order_handler import CreateOrderHandler
from handlers.decrease_stock_handler import DecreaseStockHandler
from handlers.create_payment_handler import CreatePaymentHandler
from controllers.controller import Controller
from order_saga_state import OrderSagaState

class OrderSagaController(Controller):
    """ 
    This class manages states and transitions of an order saga. The current state is persisted only in memory, as an instance variable, therefore it does not allow retrying in case the application fails.
    Please read section 11 of the arc42 document of this project to understand the limitations of this implementation in more detail.
    """

    def __init__(self):
        """ Constructor method """
        super().__init__()
        # NOTE: veuillez lire le commentaire de ce classe pour mieux comprendre les limitations de ce implémentation
        self.current_saga_state = OrderSagaState.START
        self.create_order_handler = None
        self.decrease_stock_handler = None
        self.create_payment_handler = None
        self.is_error_occurred = False

    def run(self, request):
        """ Perform steps of order saga """
        payload = request.get_json() or {}
        order_data = {
            "user_id": payload.get('user_id'),
            "items": payload.get('items', [])
        }
        self.create_order_handler = CreateOrderHandler(order_data)

        while self.current_saga_state is not OrderSagaState.END:
            # TODO: Utilisez run() ou rollback() selon les besoins.
            if self.current_saga_state == OrderSagaState.START:
                self.current_saga_state = self.create_order_handler.run()
            elif self.current_saga_state == OrderSagaState.ORDER_CREATED:
                self.decrease_stock_handler = DecreaseStockHandler(order_data['items'])
                self.current_saga_state = self.decrease_stock_handler.run()
            elif self.current_saga_state == OrderSagaState.STOCK_DECREASED:
                order_id = self.create_order_handler.order_id
                self.create_payment_handler = CreatePaymentHandler(order_id, order_data)
                self.current_saga_state = self.create_payment_handler.run()
            elif self.current_saga_state == OrderSagaState.STOCK_INCREASED:
                pass # delete order with delete_order_handler(order_id)
                self.current_saga_state = OrderSagaState.ORDER_DELETED
            elif self.current_saga_state is OrderSagaState.PAYMENT_CREATED or self.current_saga_state is OrderSagaState.ORDER_DELETED:
                self.current_saga_state = OrderSagaState.END
            else:
                self.is_error_occurred = True
                self.logger.debug(f"L'état saga n'est pas valide : {self.current_saga_state}")
                self.current_saga_state = OrderSagaState.END

        return {
            "order_id": self.create_order_handler.order_id,
            "status":  "Une erreur s'est produite lors de la création de la commande." if self.is_error_occurred else "OK"
        }



    
