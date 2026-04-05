import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Simple circuit breaker implementation to prevent cascading failures.

    Attributes:
        failure_threshold: Number of failures before tripping the circuit.
        recovery_timeout: Time in seconds to wait before attempting recovery.
        failure_count: Current count of consecutive failures.
        last_failure_time: Timestamp of the last failure.
        state: Current state of the circuit breaker (CLOSED, OPEN, HALF-OPEN).
    """
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        """Initializes the CircuitBreaker.

        Args:
            failure_threshold: Number of failures before tripping. Defaults to 5.
            recovery_timeout: Seconds to wait before recovery attempt. Defaults to 30.
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    def __call__(self, func):
        """Decorator for wrapping a function with circuit breaker logic.

        Args:
            func: The function to wrap.

        Returns:
            The wrapped function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF-OPEN"
                    logger.info(f"Circuit breaker for {func.__name__} entering HALF-OPEN state.")
                else:
                    logger.warning(f"Circuit breaker for {func.__name__} is OPEN. Skipping call.")
                    return None

            try:
                result = func(*args, **kwargs)
                if self.state == "HALF-OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    logger.info(f"Circuit breaker for {func.__name__} RESET to CLOSED.")
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                logger.error(f"Circuit breaker for {func.__name__} failure count: {self.failure_count}. Error: {e}")
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.error(f"Circuit breaker for {func.__name__} TRIPPED to OPEN.")
                
                raise e
        return wrapper

# Global instances for InfluxDB
influx_read_breaker = CircuitBreaker(failure_threshold=10, recovery_timeout=60)
influx_write_breaker = CircuitBreaker(failure_threshold=10, recovery_timeout=60)
