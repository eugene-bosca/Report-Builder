from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import reportobuster.ai_functions as ai
import reportobuster.utilities as utl
import reportobuster.send_email as se
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
#from dotenv import load_dotenv
import urllib.parse

#load_dotenv()

#Start the FastAPI app
app = FastAPI()
# Load the templates directory
templates = Jinja2Templates(directory="templates")

run_task_triggered = False

class PullRequestPayload(BaseModel):
    action: str
    pull_request: dict
    repository: dict

def run_bot_task(repo, weeks, email):
        
    # Get date range of PRs
    since, until = utl.get_dates(weeks)

    # Get PR data
    pull_request_data = utl.get_pull_request_data(repo, since, until)

    # Get PR images
    utl.get_images(pull_request_data)

    # Parse data from GitHub API
    prompt = ai.get_prompt(pull_request_data)

    # Get AI description using OPENAI and Langchain
    ai_description = ai.get_ai_description(prompt)
    
    # Format general PR info and images for email template insertion
    general_info = utl.get_general_info_dictionary(ai_description, since, until)

    # Send email via sendgrid API using dynmaic template
    se.build_and_send_email(pull_request_data, general_info, email)
    return HTMLResponse(content="Email sent!")

@app.get("/")
async def main(request: Request):
    # Render home page
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/run-task")
async def trigger_task(background_tasks: BackgroundTasks, repo: str, weeks: int, email: str):
    
    # Decode the email list
    email_list = urllib.parse.unquote(email)

    global run_task_triggered
    if not run_task_triggered:
        # Run bot task in background to avoid timeout
        run_task_triggered = True
        background_tasks.add_task(run_bot_task, repo, weeks, email_list)

    # Redirect to email sent page
    redirect_url = app.url_path_for("email_sent")
    return RedirectResponse(url=redirect_url)

@app.get("/email-sent")
async def email_sent(request: Request):

    # Render email sent page
    return templates.TemplateResponse("email_sent.html", {"request": request})

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    event = request.headers.get('X-GitHub-Event')

    if event == "pull_request":
        payload = await request.json()
        print(payload)

        webhook_payload = PullRequestPayload(**payload)

        if webhook_payload.action == "closed":

            try:
                repo = webhook_payload.repository["full_name"]
                weeks = 2
                closed_by_email = utl.get_user_email(payload['sender']['login'])
                background_tasks.add_task(run_bot_task, repo, weeks, closed_by_email)
                return {"status": "success", "message": "Report creation and email sending initiated."}
            except IncorrectTemplateEception as e:
                error_message = "Error: Incorrect template used."
                return {"status": "error", "message": error_message}

        else:
            return {"status": "success", "message": "No action taken."} 