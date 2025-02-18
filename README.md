Submittion page: https://devpost.com/software/people-coming-over

demo video https://www.youtube.com/watch?v=u6nUgXjBMuo

mock webstore we built so we didn't have to deal with 2-factor auth of amazon https://wshop-spring-water-7013.fly.dev/

## Inspiration

ai is changing how we solve problems.

when you have people coming over and your room isn't cozy
it's a huge problem that even has its own reddit https://www.reddit.com/r/malelivingspace/

previously: you ask your irl friends (if you have them) or on reddit. then waste hours shopping on websites that are just indexers that don't understand your needs, then you go through the multisep (or 1-click) click shopping experience.

**Now**:

1. you can upload it to our chat bot
2. our chatbot reasons about it, discusses what you need
3. uses a tool to buy the item to make your room better, and updates you on delivery

## What it does

tldr: image recognition, shopping discussion, tools to buy

we build a shopping site that is LLM-optimized. it takes a credit card and addresses info and mocks shipping the product.. it has instruction tuning dataset to help llms to reason about it

our chat interface analyzes the image using samba's llama3.2 11b vision model and discuses the needs of the user then it uses our custom tool to but the product and track the shipping

The chat includes an AI agent that analyzes the user’s room based on an uploaded image, providing suggestions to make it cozier and more comfortable. It identifies relevant items the user could purchase and queries ApertureDB, which uses a hybrid RAG system, to find suitable products based on user input. Authentication is handled through Stytch.

weights and bias judge checks how well model perform on connecting knowledge graph nodes and buying/tracking the product

## How we built it

- stych to sign in https://github.com/Nela62/peoplecomingover-client/blob/6fbf760d8c8289750fae4880e533ca784e6eb1cf/client/app/page.tsx#L9
- react for the chat UI and product widgets
- apertureData for storing knowledge of products and multi-step thinking with semantic connections between the nodes. https://github.com/Nela62/peoplecomingover-client/blob/main/client/api/index.py https://github.com/Nela62/peoplecomingover-client/blob/main/client/api/ApertureDB.ipynb
- hyperpocket for agents and tools
- llamaindex for running the models and tools https://github.com/Nela62/peoplecomingover-client/blob/6fbf760d8c8289750fae4880e533ca784e6eb1cf/client/api/index.py#L14
- agentql for agentic browsing of a shopping website
- fly.io for hosting and deploying the astro front end
- samba llama3.3 70b and llama3.2 11b for text and visual llms for speed https://github.com/Nela62/peoplecomingover-client/blob/6fbf760d8c8289750fae4880e533ca784e6eb1cf/client/api/index.py#L14
- we also created instructional tuning dataset for the llm-optimized product page
- our tool fills in the credit card, shipping, and billing infos on the shopping website
- accessibility features like aria and descriptive html attributes to help ai browsers navigate

## Challenges we ran into

- fly.io fastapi tutorial didn't work
- Integrating tools like LlamaIndex, ApertureDB, and Samba to work seamlessly while supporting image uploads and maintaining smooth interoperability.
- We'd need to fine-tune a model to achieve even better results. We created a dataset but ran out of time.

## Accomplishments that we're proud of

Developed a new shopping experience that helps users quickly enhance their room design, making it a space they can be proud to host in.
Created our first hybrid rag

## What we learned

how to setup hybrid rag and more about its benefits

## What's next for people-coming-over

raise a bunch of money and free people from azamon, reddit, and shopify
