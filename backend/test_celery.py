#!/usr/bin/env python3
"""
Test script for Celery task execution.
"""

import time
from celery_app import app
from tasks.example import add, long_running_task, process_deployment, monitor_service


def test_simple_task():
    print("\n=== Testing Simple Addition Task ===")
    result = add.delay(5, 3)
    print(f"Task ID: {result.id}")
    print(f"Task Status: {result.status}")

    timeout = 10
    start = time.time()
    while not result.ready() and (time.time() - start) < timeout:
        print(f"Waiting for result... Status: {result.status}")
        time.sleep(1)

    if result.ready():
        print(f"Result: {result.result}")
        print(f"Success: {result.successful()}")
    else:
        print("Task did not complete within timeout")


def test_deployment_task():
    print("\n=== Testing Deployment Task ===")
    result = process_deployment.delay("deploy-123", "my-service")
    print(f"Task ID: {result.id}")
    print(f"Task Status: {result.status}")

    timeout = 15
    start = time.time()
    while not result.ready() and (time.time() - start) < timeout:
        print(f"Waiting for result... Status: {result.status}")
        time.sleep(2)

    if result.ready():
        print(f"Result: {result.result}")
        print(f"Success: {result.successful()}")
    else:
        print("Task did not complete within timeout")


def test_monitor_task():
    print("\n=== Testing Monitor Task ===")
    result = monitor_service.delay("service-456")
    print(f"Task ID: {result.id}")
    print(f"Task Status: {result.status}")

    timeout = 10
    start = time.time()
    while not result.ready() and (time.time() - start) < timeout:
        print(f"Waiting for result... Status: {result.status}")
        time.sleep(1)

    if result.ready():
        print(f"Result: {result.result}")
        print(f"Success: {result.successful()}")
    else:
        print("Task did not complete within timeout")


if __name__ == "__main__":
    print("Testing Celery with Redis broker...")
    print(f"Broker: {app.conf.broker_url}")
    print(f"Result Backend: {app.conf.result_backend}")

    test_simple_task()
    test_monitor_task()
    test_deployment_task()

    print("\n=== All Tests Completed ===")
