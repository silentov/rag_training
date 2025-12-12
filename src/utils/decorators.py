from loguru import logger
import asyncio

from functools import wraps
from typing import Callable, ParamSpec, Type, TypeVar


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def async_retry(
    exceptions: list[Type[Exception]],
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
):
    def decorator(call: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
        @wraps(call)
        async def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            last_exception = None
            delay = base_delay

            for attempt in range(max_retries + 1):
                try:
                    return await call(*args, **kwargs)
                except tuple(exceptions) as e:
                    last_exception = e
                    if attempt >= max_retries:
                        break
                    print(e)
                    # Извлекаем статус-код, если возможно
                    status_code = getattr(e, "status_code", None)
                    rquid = getattr(e, "request_rquid", None)

                    if hasattr(e, "args") and len(e.args) > 1:
                        status_code = e.args[1]
                        rquid = e.args[2]

                    # Ретраить только при 429
                    if status_code != 429:
                        logger.warning(
                            "Исключение {}, но не 429 — не делаем retry",
                            type(e).__name__,
                        )
                        break

                    sleep_time = delay
                    if jitter:
                        sleep_time = delay * (
                            0.5 + (0.5 * asyncio.get_event_loop().time() % 1)
                        )

                    logger.warning(
                        "{}, запрос {}: попытка {} не удалась (статус {}). Повтор через {:.2f} с.",
                        call.__name__,
                        rquid,
                        attempt + 1,
                        status_code,
                        sleep_time,
                    )
                    await asyncio.sleep(sleep_time)
                    delay *= backoff_factor
            else:
                logger.error("Превышено количество попыток для {}", call.__name__)
            raise last_exception

        return wrapper

    return decorator
