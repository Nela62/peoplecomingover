#!/usr/bin/env python3

"""This is an example of how to collect pricing data from e-commerce website using AgentQL."""

import asyncio
import json
import sys

from playwright.async_api import async_playwright

import agentql

# URL of the e-commerce website
# You can replace it with any other e-commerce website but the queries should be updated accordingly
URL = "https://wshop-spring-water-7013.fly.dev/"


async def main():
    """Main function."""
    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=False
    ) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = await agentql.wrap_async(browser.new_page())
        await page.goto(URL)  # open the target URL

        form_query = """
        {
            cardName
            cardNumber
            expDate
            cvc
            billingAddress
            shippingAddress
            buy_now_btn
            delivery_date
        }
        """
        response = await page.query_elements(form_query)
        await response.cardName.fill("Kirill Igumenshchev")
        await response.cardNumber.fill("4111 1111 1111 1111")
        await response.expDate.fill("12/25")
        await response.cvc.fill("123")
        await response.billingAddress.fill("123 Elm Street, Springfield, IL, 62704")
        await response.shippingAddress.fill("456 Oak Avenue, Springfield, IL, 62704")

        # response = await page.query_elements(confirm_query)
        await response.buy_now_btn.click()

        await page.wait_for_page_ready_state()
        await page.wait_for_timeout(300)  # wait for 3 seconds
        response = await page.query_elements("{delivery_date}")
        result = {
            "delivery_date": response.delivery_date,
            "message": "Form submitted successfully!"
        }
        return result


if __name__ == "__main__":
    result = asyncio.run(main())
    print(json.dumps(result))
