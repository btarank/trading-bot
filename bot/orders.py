from bot.client import BinanceFuturesClient
from bot.validators import validate_order_inputs
from bot.logging_config import setup_logger

logger = setup_logger("orders")

# Console display helpers
DIVIDER = "=" * 50
THIN    = "-" * 50


def _print_request_summary(symbol, side, order_type, quantity, price=None, stop_price=None):
    print(f"\n{DIVIDER}")
    print("    ORDER REQUEST SUMMARY")
    print(DIVIDER)
    print(f"  Symbol      : {symbol}")
    print(f"  Side        : {side}")
    print(f"  Order Type  : {order_type}")
    print(f"  Quantity    : {quantity}")
    if price is not None:
        print(f"  Price       : {price}")
    if stop_price is not None:
        print(f"  Stop Price  : {stop_price}")
    print(DIVIDER)


def _print_order_response(response: dict):
    print("\n   ORDER PLACED SUCCESSFULLY")
    print(THIN)
    print(f"  Order ID      : {response.get('orderId', 'N/A')}")
    print(f"  Client Order  : {response.get('clientOrderId', 'N/A')}")
    print(f"  Symbol        : {response.get('symbol', 'N/A')}")
    print(f"  Side          : {response.get('side', 'N/A')}")
    print(f"  Type          : {response.get('type', 'N/A')}")
    print(f"  Status        : {response.get('status', 'N/A')}")
    print(f"  Quantity      : {response.get('origQty', 'N/A')}")
    print(f"  Executed Qty  : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price     : {response.get('avgPrice', 'N/A')}")
    if response.get("price"):
        print(f"  Limit Price   : {response.get('price')}")
    if response.get("stopPrice") and response.get("stopPrice") != "0":
        print(f"  Stop Price    : {response.get('stopPrice')}")
    print(f"  Time in Force : {response.get('timeInForce', 'N/A')}")
    print(THIN + "\n")


def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None,
) -> dict:
    """
    Command layer: orchestrates validation → placement → display.
    This is the single entry point called by the CLI.
    """

    # 1. Validate inputs
    logger.debug(
        f"Validating inputs | symbol={symbol} side={side} type={order_type} "
        f"qty={quantity} price={price} stop_price={stop_price}"
    )
    symbol, side, order_type = validate_order_inputs(
        symbol, side, order_type, quantity, price, stop_price
    )
    logger.debug("Validation passed")

    # 2. Print request summary to console
    _print_request_summary(symbol, side, order_type, quantity, price, stop_price)

    # 3. Place the order via API layer
    logger.info(
        f"Placing order | symbol={symbol} side={side} type={order_type} "
        f"qty={quantity} price={price} stop_price={stop_price}"
    )
    client = BinanceFuturesClient()
    response = client.place_order(symbol, side, order_type, quantity, price, stop_price)

    # 4. Print response to console
    _print_order_response(response)

    logger.info(
        f"Order complete | orderId={response.get('orderId')} "
        f"status={response.get('status')} executedQty={response.get('executedQty')}"
    )

    return response
