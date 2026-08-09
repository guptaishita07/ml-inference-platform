import asyncio
import time

from app.metrics import BATCH_SIZE, QUEUE_DEPTH


class DynamicBatcher:
    def __init__(self, model, batch_size=8, max_wait_ms=50):
        self.model = model
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.queue = asyncio.Queue()
        self._worker_task = None

    def start(self):
        self._worker_task = asyncio.create_task(self._worker_loop())

    async def predict(self, text: str) -> dict:
        future = asyncio.get_event_loop().create_future()

        await self.queue.put((text, future))

        # Update queue depth after enqueueing
        QUEUE_DEPTH.set(self.queue.qsize())

        return await future

    async def _worker_loop(self):
        while True:
            batch = []
            deadline = time.monotonic() + (self.max_wait_ms / 1000)

            # Wait for first request
            item = await self.queue.get()
            batch.append(item)

            # Collect additional requests
            while len(batch) < self.batch_size:
                timeout = deadline - time.monotonic()

                if timeout <= 0:
                    break

                try:
                    item = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=timeout
                    )
                    batch.append(item)

                except asyncio.TimeoutError:
                    break

            texts = [t for t, _ in batch]
            futures = [f for _, f in batch]

            # Record batch size
            BATCH_SIZE.observe(len(texts))

            # Queue size after batch removed
            QUEUE_DEPTH.set(self.queue.qsize())

            try:
                results = self.model.predict_batch(texts)

                for future, result in zip(futures, results):
                    future.set_result(result)

            except Exception as e:
                for future in futures:
                    future.set_exception(e)

            finally:
                # Final queue depth after processing
                QUEUE_DEPTH.set(self.queue.qsize())