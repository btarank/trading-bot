import click
from bot.orders import place_order
from bot.logging_config import setup_logger

logger = setup_logger("cli")

# ANSI color helpers via click.style
def green(t):  return click.style(str(t), fg="green", bold=True)
def yellow(t): return click.style(str(t), fg="yellow", bold=True)
def red(t):    return click.style(str(t), fg="red", bold=True)
def cyan(t):   return click.style(str(t), fg="cyan")
def bold(t):   return click.style(str(t), bold=True)

BANNER = f"""
{click.style('--------------------------------------', fg='cyan')}
{click.style('  ', fg='cyan')}{click.style('Binance Futures Testnet — Trading Bot', fg='yellow', bold=True)}{click.style('  ║', fg='cyan')}
{click.style('  ', fg='cyan')}{click.style('USDT-M Futures    demo-fapi.binance.com   ', fg='white')}{click.style('║', fg='cyan')}
{click.style('--------------------------------------', fg='cyan')}
"""

#  Shared order execution logic 

def _execute_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    """Confirms with user then places the order."""
    click.echo("\n" + click.style("  Confirm Order", fg="yellow", bold=True))
    click.echo(click.style("  " + "─" * 40, fg="yellow"))
    click.echo(f"  Symbol     : {bold(symbol)}")
    click.echo(f"  Side       : {green(side) if side == 'BUY' else red(side)}")
    click.echo(f"  Type       : {cyan(order_type)}")
    click.echo(f"  Quantity   : {bold(quantity)}")
    if price:
        click.echo(f"  Price      : {bold(price)}")
    if stop_price:
        click.echo(f"  Stop Price : {bold(stop_price)}")
    click.echo(click.style("  " + "─" * 40, fg="yellow"))

    if not click.confirm("\n  Proceed with this order?", default=True):
        click.echo(yellow("\n  Order cancelled.\n"))
        return

    click.echo(cyan("\n  Placing order..."))

    logger.info(
        f"CLI invoked | symbol={symbol} side={side} type={order_type} "
        f"qty={quantity} price={price} stop_price={stop_price}"
    )

    try:
        place_order(symbol, side, order_type, quantity, price, stop_price)
    except ValueError as e:
        click.echo(f"\n  {red('  Validation Error:')} {e}\n", err=True)
        logger.warning(f"Validation error | {e}")
    except EnvironmentError as e:
        click.echo(f"\n  {red('  Config Error:')} {e}\n", err=True)
        logger.error(f"Environment error | {e}")
    except Exception as e:
        click.echo(f"\n  {red('  Order Failed:')} {e}\n", err=True)
        logger.error(f"Unhandled exception | {type(e).__name__}: {e}")


#  Interactive menu 

def _interactive_menu():
    """Walks user through order placement step by step."""
    click.clear()
    click.echo(BANNER)
    click.echo(bold("  Interactive Order Placement\n"))

    # Symbol
    symbol = click.prompt(
        cyan("  Enter symbol"),
        default="BTCUSDT",
    ).upper().strip()

    # Side
    click.echo(f"\n  Select side:")
    click.echo(f"    {green('1')} — BUY")
    click.echo(f"    {red('2')} — SELL")
    side_choice = click.prompt(cyan("  Choice"), type=click.Choice(["1", "2"]), show_choices=False)
    side = "BUY" if side_choice == "1" else "SELL"

    # Order type
    click.echo(f"\n  Select order type:")
    click.echo(f"    {cyan('1')} — MARKET      (executes immediately at best price)")
    click.echo(f"    {cyan('2')} — LIMIT        (executes at your specified price)")
    click.echo(f"    {cyan('3')} — STOP_MARKET  (triggers at stop price, executes at market)")
    type_choice = click.prompt(cyan("  Choice"), type=click.Choice(["1", "2", "3"]), show_choices=False)
    order_type = {"1": "MARKET", "2": "LIMIT", "3": "STOP_MARKET"}[type_choice]

    # Quantity
    quantity = click.prompt(cyan("\n  Enter quantity"), type=float)

    # Price (LIMIT only)
    price = None
    if order_type == "LIMIT":
        price = click.prompt(cyan("  Enter limit price"), type=float)

    # Stop price (STOP_MARKET only)
    stop_price = None
    if order_type == "STOP_MARKET":
        stop_price = click.prompt(cyan("  Enter stop trigger price"), type=float)

    _execute_order(symbol, side, order_type, quantity, price, stop_price)


#  CLI entry point 

@click.command()
@click.option("--symbol",     default=None, help="Trading pair, e.g. BTCUSDT")
@click.option("--side",       default=None, type=click.Choice(["BUY", "SELL"], case_sensitive=False), help="BUY or SELL")
@click.option("--order-type", "order_type", default=None,
              type=click.Choice(["MARKET", "LIMIT", "STOP_MARKET"], case_sensitive=False),
              help="MARKET, LIMIT, or STOP_MARKET")
@click.option("--quantity",   default=None, type=float, help="Order quantity")
@click.option("--price",      default=None, type=float, help="Limit price (LIMIT orders)")
@click.option("--stop-price", "stop_price", default=None, type=float, help="Trigger price (STOP_MARKET orders)")
def main(symbol, side, order_type, quantity, price, stop_price):
    """
    Binance Futures Testnet Trading Bot

    \b
    Run with no arguments for interactive mode:
      python cli.py

    \b
    Or pass arguments directly:
      python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.002
      python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.002 --price 80000
      python cli.py --symbol BTCUSDT --side BUY --order-type STOP_MARKET --quantity 0.002 --stop-price 66000
    """
    click.echo(BANNER)

    # If no args passed -> launch interactive mode
    if not all([symbol, side, order_type, quantity]):
        _interactive_menu()
        return

    _execute_order(symbol, side, order_type, quantity, price, stop_price)


if __name__ == "__main__":
    main()