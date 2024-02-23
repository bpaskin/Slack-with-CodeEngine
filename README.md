# Abyssumpy
Python function that reads messages from a Slack channel. Collects the messages, replies, dates of messages and replies, and reactions.

---
Requires Python 3.11 

---
#### Output in JSON format
```
{'timestamp': '1707948017.791379', 'date': '2024-02-14, 22:00:17 +0000', 'message': 'Idea - Market Sentiment Analysis: Analyze social media and news sources using natural language processing (NLP) to gauge market sentiment and inform investment decisions', 'reactions': 5, 'replies': [{'timestamp': '1707949127.205179', 'date': '2024-02-14, 22:18:47 +0000', 'message': 'Provides a more nuanced understanding of market dynamics, potentially leading to better investment decisions.', 'reactions': 2}, {'timestamp': '1707949131.303139', 'date': '2024-02-14, 22:18:51 +0000', 'message': 'Sentiment analysis might be swayed by social media manipulation or misinformation.', 'reactions': 0}, {'timestamp': '1707949136.355069', 'date': '2024-02-14, 22:18:56 +0000', 'message': 'Real-time sentiment analysis could give traders an edge in volatile markets.', 'reactions': 0}]}, {'timestamp': '1707948011.060469', 'date': '2024-02-14, 22:00:11 +0000', 'message': 'Idea - Predictive Analytics for Customer Behavior: Employ machine learning to analyze customer data and predict future behaviors, such as loan defaults or investment trends, allowing for proactive management.', 'reactions': 3, 'replies': [{'timestamp': '1707949110.673709', 'date': '2024-02-14, 22:18:30 +0000', 'message': 'Predictive insights could lead to more personalized and effective customer services.', 'reactions': 0}, {'timestamp': '1707949114.888899', 'date': '2024-02-14, 22:18:34 +0000', 'message': 'Reliance on historical data might not always accurately predict future behavior, especially in unprecedented scenarios.', 'reactions': 0}, {'timestamp': '1707949119.737209', 'date': '2024-02-14, 22:18:39 +0000', 'message': 'Could significantly reduce default rates and optimize product offerings.', 'reactions': 0}]}, {'timestamp': '1707948004.534279', 'date': '2024-02-14, 22:00:04 +0000', 'message': 'Idea - Operational Efficiency: Use AI to automate repetitive and time-consuming processes, such as data entry and report generation, increasing operational efficiency.', 'reactions': 0, 'replies': [{'timestamp': '1707949089.141289', 'date': '2024-02-14, 22:18:09 +0000', 'message': 'Automating routine tasks could free up employees to focus on more strategic activities.', 'reactions': 0}, {'timestamp': '1707949094.313279', 'date': '2024-02-14, 22:18:14 +0000', 'message': 'There’s a risk of job displacement for those currently performing manual tasks.', 'reactions': 0}, {'timestamp': '1707949100.235439', 'date': '2024-02-14, 22:18:20 +0000', 'message': 'The long-term savings and efficiency gains could be substantial.', 'reactions': 0}]}, {'timestamp': '1707947999.697139', 'date': '2024-02-14, 21:59:59 +0000', 'message': 'Idea - Customer Service Chatbots: Deploy AI-powered chatbots to handle routine customer inquiries, improving response times and freeing human agents to address more complex issues.', 'reactions': 6, 'replies': [{'timestamp': '1707949069.898819', 'date': '2024-02-14, 22:17:49 +0000', 'message': 'Chatbots could significantly improve customer satisfaction through 24/7 service', 'reactions': 0}, ...
```

---
## Adding an application to Slack

Each company/indivdual process is going to be different.  Follow your organisations information.

1. After the workspace is setup, ceate a [new application](https://api.slack.com/apps) > New Application (Button) > From Scratch 
   * Fill in the name of the application
   * Fill in the test workspace name
   * Click Create Application Button
2. Select OAuth and Permissions on the left hand side
   * Add the proper scopes needed for the bot
3. If not using a webhook, then go into the channels and invite the bot
```
/invite @bot_name
```
4. Code your bot!

---

## Deploying to Code Engine

### Logon and prepare client
1. Logon to IBM Cloud
```
ibmcloud login -u <user_name>
```
2. Choose correct account from the list
3. List resource groups 
```
ibmcloud resource groups
```
4. Choose which resource group to use
```
ibmcloud target -g <group name>
```
5. Choose region
```
ibmcloud target -r <region name>
```
6. Install the plugin
```
ibmcloud plugin install code-engine
```
7. List the plugins
```
ibmcloud plugin list
```
8. Show the Code Engine plugin
```
ibmcloud plugin show code-engine
```
9. Update plugin, if necessary
```
ibmcloud plugin update <name>
```

### Deploy the function
1. Download the code locally and go into the directory where the `abyssum.py`
2. Create a Code Engine project
```
ibmcloud ce project create -n Abyssum
```
3. Create the function and and upload it to IBM Cloud
```
ibmcloud ce fn create  --name abyssumpy --build-source . -runtime python-3.11 -e SLACK_TOKEN=<Slack OAuth Token> -e CHANNEL_ID=<Slack Channel ID> 
```

If everything goes well, then the function will be deployed and a URL to the application will be shown.

Updating the application:
```
ibmcloud ce fn update  --name abyssumpy --build-source . -runtime python-3.11 
```

### Other commands
Get application information
```
ibmcloud ce fn get -n abyssumpy
```

Get the logs from all containers
```
ibmcloud ce fn logs -n abyssumpy
```

