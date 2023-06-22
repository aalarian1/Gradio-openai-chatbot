import openai, os
import gradio as gr
import pandas as pd
import numpy as np
# Initialize the API key
openai.api_key = "ENTER-API-KEY"

finetune_history = [
                {"role": "user", "content": f"You are director of NLP at OpenAI and conversation specialist. You are building a self learning chatbot agent with conditional language model with a dataset of input-output pairs for training data. You are also an expert arabic translator. if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"You are not allowed to write code. if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"You are trying to build a self learning chatbot agent with conditional language model with a dataset of input-output pairs for training data. if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"Use case: Provide user with functionality to create new dashboard and reports. Description: Chatbot will allow users to request new dashboards and reports bearing in mind the need for validation of the content pulled from various integratabtle data sources. if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"Use case: Allowing user to inquire anything in terms of data in our systems , check status of submitted requests, send emails , report sharing, Data analytics, and graph creation. Description: Chatbot shall serve as inquiry providers for all the parts of the scope. Data, request status,  number of requests, request duration, This is a smart BOT besides the use cases, you team must identify missing use cases and use a nlp language model to solve the missing use cases. gpt3, davinci03. Any question to the Bot (conversation) and questions are logged in message history, and unanswered questions will be available for review by the Admin role, to be decided if this conversations will be available as a function inside the Bot. if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"Use Case: Chatbot will load actions and permission should be reflected as per the privileges, Also Chatbot will load user profile data and configure available functionality based on user profile. Description: Chatbot will handle each action inquires, and any request should be based on the user privileges and permissions.  Available functionality will be also available based on privileges.  So all the UI  menus must be identified in the portal and  is varying per user. Menus are accessible based on user authorization. if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"Use case: Chatbot will be able to generate/provide descriptive insights with rich contexts. Description: Chatbot to provide narratives, charts,  when requiring data. Moreover, it should have the ability to share through email or any possible mediums, based on data models built in integratabtle data sources. if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"For each prompted task you are to rewrite this prompt and arrange in intent table per tokenizable word. Intent table has headers Order, intent, platform, parameters, summary, response.\n Headers Definitions: Order : numbered ordering of task if multiple tasks asked in same prompt, Integer. Intent: intent type to be chosen fro these options: Task Specification, Data Analysis, Data Integration, Data Fetch, Communication/Scheduling, Report Creation, Report Request, Report Deletion, Dashboard Creation, Dashboard Fetch, Chart Creation, Table Creation. Platform: platform specified in the request to use for task. i.e Gmail, MYSQL, etc.. Parameters: parameters to be used in platform Summary: summary of what is to be done. Response: this is the gpt expert response of how to do task. Re write each requirement in prompt to reflect intent for each task in order of text.  if you understand reply OK?"},
                   {"role": "assistant", "content": f"OK"},
                   {"role": "user", "content": f"Can you fetch the table MEDIUM_Packages fro our potsgreSQL database? If found find the packages with status_submitted date equals to todays date. Can you then send the found results in email to ahmed@gmail.com with SUBJECT: Daily Spend and Body: data found"},
                   {"role": "assistant", "content": f"Order: 3\nIntent: Data Fetch, Communication/Scheduling\nPlatform: PostgreSQL, Gmail\nParameters:\n- Table name: MEDIUM_Packages\n- Email recipient: ahmed@gmail.com\n- Email subject: Daily Spend\n- Email body: Data found\n- Status_submitted date: Today’s date\nSummary:\nThe chatbot should fetch the MEDIUM_Packages table from the PostgreSQL database and find the packages with a status_submitted date equals to today’s date. Then, the chatbot should send the results in an email to ahmed@gmail.com with the subject as “Daily Spend” and the body as “data found”.\nResponse:\nTo fetch the MEDIUM_Packages table from the PostgreSQL database and find the packages with a status_submitted date equals to today’s date and send the results to ahmed@gmail.com via email, follow these steps:\n1. Access the PostgreSQL database.\n2. In the SQL editor, input: SELECT * FROM MEDIUM_Packages WHERE status_submitted_date = CURRENT_DATE;\n3. Execute the query.\n4. Save the result of the query.\n5. Open your Gmail account.\n6. Write a new email.\n7. Input ahmed@gmail.com as the recipient.\n8. In the subject field, input “Daily Spend”.\n9. In the body of the email, input “data found”.\n10. Attached the result of the query to the email.\n11. Send the email.\n"},
                   {"role": "user", "content": f"I want you to email  example@gmail.com with Subject: MS TEAMS MEETING and setup a ms teams invitation link for me and him for tuesday, march 20th 2023 and link it in BODY"},
                   {"role": "assistant", "content": f"Order: 2\nIntent: Communication/Scheduling\nPlatform: Gmail, MS Teams\nParameters:\n- Email recipient: example@gmail.com\n- Email subject: MS TEAMS MEETING\n- Meeting date: Tuesday, March 20th, 2023\n- MS Teams invitation link\nSummary:\nThe chatbot should send an email to example@gmail.com with the subject as “MS TEAMS MEETING”. The email should also contain a link to a MS Teams invitation for a meeting scheduled for Tuesday, March 20th, 2023.\nResponse:\nTo send an email to example@gmail.com with the subject as “MS TEAMS MEETING” and a MS Teams invitation link for a meeting scheduled for Tuesday, March 20th, 2023, follow these steps:\n1. Open your Gmail account.\n2. Click on “Compose” to create a new email.\n3. Enter example@gmail.com in the recipient field.\n4. In the subject field, input “MS TEAMS MEETING”.\n5. In the body of the email, insert a MS Teams invitation link for the meeting that is scheduled for Tuesday, March 20th, 2023.\n6. Click “Send” to send the email."},
                   {"role": "user", "content": f"From file CaseInfo.csv find CaseClosingTime of when CaseInfoID = 881 and CaseNumber= JD0207121 and send an email to g@mail.com with title: found and body: insert value found from csv"},
                   {"role": "assistant", "content": f"Order: 1 Intent: Data Fetch Platform: CSV Parameters: - File name: CaseInfo.csv - Header1 name: CaseInfoID -Header1 value: 881 - Header2: CaseNumber Header2 value: JD0207121 Summary: The chatbot should fetch the CaseClosingTime value when CaseInfoID=881 and CaseNumber=JD0207121 from the CaseInfo.csv file. Response: To fetch the CaseClosingTime value of CaseInfoID=881 and CaseNumber=JD0207121 from the CaseInfo.csv file follow these steps: 1. Open the CaseInfo.csv file. 2. Using the appropriate CSV reader, filter the rows where the CaseInfoID is 881 and where the CaseNumber is JD0207121. 3. Retrieve the CaseClosingTime value from the filtered row. Order: 2 Intent: Communication/Scheduling Platform: Gmail Parameters: - Email recipient: g@mail.com - Email subject: found - Email body: value found from csv Summary: The chatbot should send an email to g@mail.com with the subject as “found” and the body as “value found from csv”. Response: To send an email to g@mail.com with the subject as “found” and  insert the CaseClosingTime value fetched, follow these steps: 1. Open your Gmail account. 2. Write a new email. 3. Input g@mail.com as the recipient. 4. the subject field, input “found”. 5. In the body of the email, input “value found from csv”. 6. In the same email body, input the CaseClosingTime value that was retrieved from the CSV file. 7. Send the email."},
                   {"role": "user", "content": f"DATA"},
                   {"role": "assistant", "content": f"Pick Operation:\n-GET\n-DELETE\n-UPDATE"},
                   {"role": "user", "content": f"GET"},
                   {"role": "assistant", "content": f"Pick Platform:\n-PostgreSQL\n-MYSQL\n-S3"},
                   {"role": "user", "content": f"Postgres"},
                   {"role": "assistant", "content": f"Insert Databse Name:"},
                   {"role": "user", "content": f"Cases"},
                   {"role": "assistant", "content": f"Insert Table Name:"},
                   {"role": "user", "content": f"CaseStudies"},
                   {"role": "assistant", "content": f"**prompt-> inset databse pulled from data integration piepline based on selection**"},
                   {"role": "user", "content": f"DASHBOARD"},
                   {"role": "assistant", "content": f"Pick Operation:\nCreate\nFetch\nCharts\nTables\n-Analysis"},
                   {"role": "user", "content": f"Fetch"},
                   {"role": "assistant", "content": f"Pick Platform:\n-Power BI\n-Qlik Sense"},
                   {"role": "user", "content": f"Power BI *or BI"},
                   {"role": "assistant", "content": f"Insert Dashboard Name:"},
                   {"role": "user", "content": f"Dashboard1"},
                   {"role": "assistant", "content": f"Insert Data Export Type"},
                   {"role": "user", "content": f"Linear Regression"},
                   {"role": "assistant", "content": f"**prompt-> explain process of pulling a dashboard from selected platform. inset dashboard data pulled from dashboard integration piepline based on selection of file type**"},
                   
                   ]
message_history = []
flag = False
pipeline_history = {}
def predict(input):
    
    #tokenize the new input sentence
    # message_history.append({"role": "user", "content": f"{input}"})
    finetune_history.append({"role": "user", "content": f"{input}"})
    s_data = input.replace(" ", "")
    print(s_data)
    # This ill be a linked list with pipeline replies and save position in linked list per pipeline so as we talk we could always pull history
    if 'DATA' == s_data or flag==True:
        # pipeline_history[s_data] = {}
        reply_content = "Pick Operation:\n-GET\n-DELETE\n-UPDATE"
    elif 'COMM/SCH' == s_data.lower():
        reply_content = "Pick Operation:\n-Email\n-Microsoft Teams"

    elif 'REPORT' == s_data.lower():
        reply_content = "Pick Operation:\nCreate\nDelete\nFetch\nUpdate"

    elif 'DASHBOARD' == s_data.lower():
        reply_content = "Pick Operation:\nCreate\nFetch\nCharts\nTables\n-Analysis"
    # elif 'postgres' == s_data.lower() or 'postgresql'==s_data.lower() or 'mysql' == s_data.lower() or 's3'==s_data.lower():
    #     import pandas as pd
    #     df = pd.read_csv('/Users/adeek/Downloads/openai-quickstart-node/CaseInfo.csv')
    #     reply_content = df.head()
        # print(df.dtypes())
        # flag = True
       

    else:
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", #10x cheaper than davinci, and better. $0.002 per 1k tokens
        messages=finetune_history
        )
        #GPT reply:
        reply_content = completion.choices[0].message.content#.replace('```python', '<pre>').replace('```', '</pre>')
        # resp_content = reply_content.split('\nResponse:\n')
        # print(resp_content)
        # gpt_response = resp_content[1]
        # intent = reply_content[reply_content.find('\nIntent:')+len('\nIntent:'):reply_content.rfind('\nPlatform:')].split(',')
        # print(intent)
        # platforms = reply_content[reply_content.find('\nPlatform:')+len('\nPlatform:'):reply_content.rfind('\nParameters:\n')].split(',')
        # print(platforms)
        # params= reply_content[reply_content.find('\nParameters:\n')+len('\nParameters:\n'):reply_content.rfind('\nSummary:\n')].split('\n')
        # print(params)
        # summary= reply_content[reply_content.find('\nSummary:\n')+len('\nSummary:\n'):reply_content.rfind('\nResponse:\n')]
        # print(summary)
        # print(reply_content, resp_content)
        # print(intent + '/n'+platforms + '/n' +params,summary)
    finetune_history.append({"role": "assistant", "content": f"{reply_content}"}) 


    # message_history.append({"role": "assistant", "content": f"{gpt_response}"}) 
    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    # response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)]  # convert to tuples of list
    response = [(finetune_history[i]["content"], finetune_history[i+1]["content"]) for i in range(0, len(finetune_history)-1, 2)]  # convert to tuples of list
    # print(finetune_history)
    # print(message_history)
    return response


# def get_data():
#     URL = "https://docs.google.com/spreadsheets/d/1UoKzzRzOCt-FXLLqDKLbryEKEgllGAQUEJ5qtmmQwpU/edit#gid=0"
#     csv_url = URL.replace('/edit#gid=', '/export?format=csv&gid=')
#     return pd.read_csv(csv_url)
# def change_textbox(choice):
#     if choice == "short":
#         return "short"
#     elif choice == "long":
#         return "long"
#     else:
#         return "none" #gr.Textbox.update(visible=False)


# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo: 
    # radio = gr.Radio(["short", "long", "none"], label="What kind of essay would you like to write?")
    # text = gr.Textbox(lines=2, interactive=True).style(show_copy_button=True)

    # btn = gr.Button("data")
    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot(value=[["Hey! How's it going?",None]])
    
    # radio.change(fn=change_textbox, inputs=radio, outputs=text) 

    # creates a new Row component, which is a container for other components.
    with gr.Row(): 
        '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
        txt = gr.Textbox(show_label=True, placeholder="Enter text and press enter").style(container=False)
        '''
        sets the submit action of the Textbox to the predict function, 
        which takes the input from the Textbox, the chatbot instance, 
        and the state instance as arguments. 
        This function processes the input and generates a response from the chatbot, 
        which is displayed in the output area.'''
        
        txt.submit(predict, txt, chatbot) # submit(function, input, output)
        #txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string 

        '''
        sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
        This line is equivalent to the commented out line above, but uses a different implementation. 
        The _js parameter is used to pass a JavaScript function to the submit method.'''
        txt.submit(None, None, txt, _js="() => {''}") # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.
            
    demo.launch(debug=True)
