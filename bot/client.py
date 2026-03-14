import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger("client")

# Demo Trading API base URL
BASE_URL = "https://demo-fapi.binance.com"

class BinanceFuturesClient:
    """
    API layer: direct REST calls to Binance Futures Testnet.
    Uses HMAC-SHA256 signing for authenticated endpoints.
    Handles auth, request logging, and raw API errors.
    All business logic lives in orders.py, not here.
    """

    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise EnvironmentError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file.\n"
                "Get your keys from the Demo Trading API page on testnet.binancefuture.com"
            )

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
        })
        logger.info(f"BinanceFuturesClient initialized | base_url={BASE_URL}")

    def _sign(self, params: dict) -> dict:
        """Adds timestamp and HMAC-SHA256 signature to params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None,
        stop_price: float = None,
    ) -> dict:
        """
        Constructs and signs the order request, sends it to the Futures Testnet,
        logs full request and response, and returns the response dict.
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        if order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price

        signed_params = self._sign(params)
        logger.info(f"API REQUEST  | POST /fapi/v1/order | params={params}")

        try:
            response = self.session.post(
                f"{BASE_URL}/fapi/v1/order",
                params=signed_params,
            )
            data = response.json()

            if response.status_code != 200:
                code = data.get("code", response.status_code)
                msg = data.get("msg", "Unknown error")
                logger.error(
                    f"API ERROR    | status_code={response.status_code} | "
                    f"code={code} | message={msg}"
                )
                raise Exception(f"APIError(code={code}): {msg}")

            logger.info(f"API RESPONSE | success | response={data}")
            return data

        except Exception as e:
            if "APIError" in str(e):
                raise
            logger.error(f"UNEXPECTED ERROR | {type(e).__name__} | {str(e)}")
            raise