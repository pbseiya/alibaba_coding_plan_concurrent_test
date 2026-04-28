#!/usr/bin/env python3
"""
Concurrent test for Alibaba Coding Plan API.
"""

import asyncio
import time
from dataclasses import dataclass, field
from aiohttp import ClientSession, ClientTimeout
from config import API_URL, CONCURRENCY_LEVEL, TOTAL_REQUESTS, TIMEOUT_SECONDS, DEFAULT_PAYLOAD, DEFAULT_HEADERS


@dataclass
class TestResult:
    """Store test execution results."""
    success: int = 0
    failed: int = 0
    total_time: float = 0.0
    response_times: list = field(default_factory=list)
    completion_times: list = field(default_factory=list)  # absolute timestamps
    errors: list = field(default_factory=list)


async def make_request(session: ClientSession, request_id: int, result: TestResult, test_start: float) -> None:
    """Make a single API request."""
    start_time = time.time()
    try:
        async with session.post(
            API_URL,
            json=DEFAULT_PAYLOAD,
            headers=DEFAULT_HEADERS
        ) as response:
            response_time = time.time() - start_time
            result.response_times.append(response_time)
            result.total_time += response_time
            result.completion_times.append(time.time() - test_start)

            if response.status == 200:
                result.success += 1
            else:
                result.failed += 1
                error_msg = f"Request {request_id}: HTTP {response.status}"
                result.errors.append(error_msg)
                print(f"⚠ {error_msg}")

    except Exception as e:
        result.failed += 1
        response_time = time.time() - start_time
        result.response_times.append(response_time)
        result.completion_times.append(time.time() - test_start)
        result.errors.append(f"Request {request_id}: {str(e)}")
        print(f"✗ Request {request_id} failed: {e}")


async def run_concurrent_test(concurrency: int, total: int) -> TestResult:
    """Run concurrent API tests."""
    result = TestResult()
    
    timeout = ClientTimeout(total=TIMEOUT_SECONDS)
    async with ClientSession(timeout=timeout) as session:
        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(concurrency)
        
        async def bounded_request(request_id: int):
            async with semaphore:
                await make_request(session, request_id, result, start_time)

        tasks = [bounded_request(i) for i in range(total)]

        start_time = time.time()
        await asyncio.gather(*tasks)
        total_elapsed = time.time() - start_time

    # --- คำนวณ Peak Requests/sec (สูงสุดต่อวินาที) ---
    peak_rps = 0
    if result.completion_times:
        sorted_times = sorted(result.completion_times)
        # ใช้ sliding window 1 วินาที หาจุดที่มีคำขอเสร็จมากที่สุด
        window = 1.0
        left = 0
        for right in range(len(sorted_times)):
            while sorted_times[right] - sorted_times[left] > window:
                left += 1
            count_in_window = right - left + 1
            if count_in_window > peak_rps:
                peak_rps = count_in_window

    # Print results
    print("\n" + "="*60)
    print("📊 CONCURRENT TEST RESULTS")
    print("="*60)
    print(f"Total requests:     {total}")
    print(f"Concurrency level:  {concurrency}")
    print(f"Successful:         {result.success} ✓")
    print(f"Failed:             {result.failed} ✗")
    print(f"Total time:         {total_elapsed:.3f}s")
    
    if result.response_times:
        avg_time = sum(result.response_times) / len(result.response_times)
        min_time = min(result.response_times)
        max_time = max(result.response_times)
        print(f"Avg response time:  {avg_time:.3f}s")
        print(f"Min response time:  {min_time:.3f}s")
        print(f"Max response time:  {max_time:.3f}s")
        print(f"Requests/sec:       {total/total_elapsed:.2f}")
        print(f"Peak requests/sec:  {peak_rps} (สูงสุด 1 วินาที)")
    
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(result.errors) > 10:
            print(f"  ... and {len(result.errors) - 10} more")
    
    print("="*60)
    
    return result


def main():
    """Main entry point."""
    print(f"🚀 Starting concurrent test for Alibaba Coding Plan API")
    print(f"   URL: {API_URL}")
    print(f"   Requests: {TOTAL_REQUESTS}, Concurrency: {CONCURRENCY_LEVEL}")
    print(f"   Timeout: {TIMEOUT_SECONDS}s\n")
    
    asyncio.run(run_concurrent_test(CONCURRENCY_LEVEL, TOTAL_REQUESTS))


if __name__ == "__main__":
    main()
