VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_MARKET"]


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None,
) -> tuple:
    """
    Validates all CLI inputs before sending to the API.
    Raises ValueError with a descriptive message on any failure.
    Returns normalized (symbol, side, order_type) tuple.
    """
    symbol = symbol.upper().strip()
    side = side.upper().strip()
    order_type = order_type.upper().strip()

    # Symbol validation
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    if not symbol.endswith("USDT"):
        raise ValueError(
            f"Symbol '{symbol}' must end with USDT (e.g. BTCUSDT, ETHUSDT)."
        )

    # Side validation
    if side not in VALID_SIDES:
        raise ValueError(
            f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}"
        )

    # Order type validation
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}"
        )

    # Quantity validation
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")

    # LIMIT-specific validation
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError(
                "LIMIT orders require a --price greater than 0."
            )

    # STOP_MARKET-specific validation
    if order_type == "STOP_MARKET":
        if stop_price is None or stop_price <= 0:
            raise ValueError(
                "STOP_MARKET orders require a --stop-price (the trigger price) greater than 0."
            )

    return symbol, side, order_type