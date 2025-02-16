#!/usr/bin/env python3

"""This is an example of how to collect pricing data from e-commerce website using AgentQL."""

import asyncio

from playwright.async_api import async_playwright
import json
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

        with open('mock_data.json', 'r') as f:
            form_data = json.load(f)

        form_query = """
        {
            first_name
            last_name
            email
            subject_of_inquiry
            inquiry_text_box
            submit_btn
        }
        """
        response = await page.query_elements(form_query)

        await response.first_name.fill(form_data["first_name"])
        await response.last_name.fill(form_data["last_name"])
        await response.email.fill(form_data["email"])
        await response.subject_of_inquiry.select_option(label=form_data["subject_of_inquiry"])
        await response.inquiry_text_box.fill(form_data["inquiry_text_box"])

        # Submit the form
        await response.submit_btn.click()

        # confirm form
        confirm_query = """
        {
            confirmation_btn
        }
        """

        response = await page.query_elements(confirm_query)
        await response.confirmation_btn.click()
        await page.wait_for_page_ready_state()
        await page.wait_for_timeout(3000)  # wait for 3 seconds
        print("Form submitted successfully!")


if __name__ == "__main__":
    asyncio.run(main())
