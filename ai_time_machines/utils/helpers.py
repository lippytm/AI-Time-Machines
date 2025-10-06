"""Utility functions for AI Time Machines."""

import asyncio
import logging
import time
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from functools import wraps
from datetime import datetime, timedelta

T = TypeVar('T')


def setup_logging(level: str = "INFO", format_string: Optional[str] = None) -> None:
    """Setup logging configuration."""
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def retry_async(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying async functions."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = delay * (backoff ** attempt)
                        await asyncio.sleep(wait_time)
                    else:
                        break
            
            # If we get here, all retries failed
            raise last_exception
        
        return wrapper
    return decorator


def timeout_async(timeout_seconds: float):
    """Decorator for adding timeout to async functions."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout_seconds)
        return wrapper
    return decorator


class RateLimiter:
    """Rate limiter for controlling function call frequency."""
    
    def __init__(self, max_calls: int, time_window: float):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """Acquire permission to make a call."""
        async with self._lock:
            now = time.time()
            # Remove old calls outside the time window
            self.calls = [call_time for call_time in self.calls if now - call_time < self.time_window]
            
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
            return False
    
    async def wait_and_acquire(self) -> None:
        """Wait until permission is available, then acquire it."""
        while not await self.acquire():
            await asyncio.sleep(0.1)


class CircuitBreaker:
    """Circuit breaker pattern implementation for resilient components."""
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """Execute a function through the circuit breaker."""
        async with self._lock:
            if self.state == "open":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "half-open"
                else:
                    raise Exception("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            async with self._lock:
                if self.state == "half-open":
                    self.state = "closed"
                    self.failure_count = 0
            return result
        except Exception as e:
            async with self._lock:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
            raise e


class AsyncCache:
    """Simple async cache with TTL support."""
    
    def __init__(self, default_ttl: float = 300.0):
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() < entry["expires_at"]:
                    return entry["value"]
                else:
                    del self._cache[key]
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set value in cache."""
        if ttl is None:
            ttl = self.default_ttl
        
        async with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": time.time() + ttl
            }
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
        return False
    
    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()
    
    async def cleanup_expired(self) -> int:
        """Remove expired entries and return count of removed items."""
        now = time.time()
        expired_keys = []
        
        async with self._lock:
            for key, entry in self._cache.items():
                if now >= entry["expires_at"]:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
        
        return len(expired_keys)


def format_timestamp(timestamp: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format timestamp to string."""
    return timestamp.strftime(format_string)


def parse_timestamp(timestamp_str: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse string to timestamp."""
    return datetime.strptime(timestamp_str, format_string)


def time_delta_to_seconds(delta: Union[timedelta, str, int, float]) -> float:
    """Convert various time representations to seconds."""
    if isinstance(delta, timedelta):
        return delta.total_seconds()
    elif isinstance(delta, str):
        # Simple parsing for strings like "5m", "1h", "30s"
        if delta.endswith('s'):
            return float(delta[:-1])
        elif delta.endswith('m'):
            return float(delta[:-1]) * 60
        elif delta.endswith('h'):
            return float(delta[:-1]) * 3600
        elif delta.endswith('d'):
            return float(delta[:-1]) * 86400
        else:
            return float(delta)  # Assume seconds
    else:
        return float(delta)


class HealthChecker:
    """Health checking utility for components."""
    
    def __init__(self):
        self.checks: Dict[str, Callable[[], bool]] = {}
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def register_check(self, name: str, check_func: Callable[[], bool]) -> None:
        """Register a health check function."""
        self.checks[name] = check_func
        self._logger.debug(f"Registered health check: {name}")
    
    def unregister_check(self, name: str) -> None:
        """Unregister a health check."""
        if name in self.checks:
            del self.checks[name]
            self._logger.debug(f"Unregistered health check: {name}")
    
    async def run_all_checks(self) -> Dict[str, bool]:
        """Run all registered health checks."""
        results = {}
        for name, check_func in self.checks.items():
            try:
                results[name] = await self._run_check(check_func)
            except Exception as e:
                self._logger.error(f"Health check {name} failed with error: {e}")
                results[name] = False
        return results
    
    async def _run_check(self, check_func: Callable[[], bool]) -> bool:
        """Run a single health check."""
        if asyncio.iscoroutinefunction(check_func):
            return await check_func()
        else:
            return check_func()
    
    async def is_healthy(self) -> bool:
        """Check if all health checks pass."""
        results = await self.run_all_checks()
        return all(results.values())


class Metrics:
    """Simple metrics collection."""
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}
        self.timers: Dict[str, list] = {}
        self._lock = asyncio.Lock()
    
    async def increment_counter(self, name: str, value: int = 1) -> None:
        """Increment a counter metric."""
        async with self._lock:
            self.counters[name] = self.counters.get(name, 0) + value
    
    async def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge metric."""
        async with self._lock:
            self.gauges[name] = value
    
    async def record_timer(self, name: str, duration: float) -> None:
        """Record a timer metric."""
        async with self._lock:
            if name not in self.timers:
                self.timers[name] = []
            self.timers[name].append(duration)
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        async with self._lock:
            return {
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
                "timers": {name: {
                    "count": len(values),
                    "avg": sum(values) / len(values) if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0
                } for name, values in self.timers.items()}
            }
    
    async def reset_metrics(self) -> None:
        """Reset all metrics."""
        async with self._lock:
            self.counters.clear()
            self.gauges.clear()
            self.timers.clear()