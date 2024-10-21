
from fastapi import APIRouter
import os
import resend

RESEND_KEY = os.getenv('RESEND_KEY')
resend.api_key = RESEND_KEY
router = APIRouter()

@router.post("/")
async def create_proceso():
  
  params: resend.Emails.SendParams = {
    "from": "Nicolas <onboarding@resend.dev>",
    "to": ["nhenaoz@unicartagena.edu.co"],
    "subject": "Hello World!",
    "html": "<p>Oh yeah, Diamantes...</p>"
  }

  email = resend.Emails.send(params)
  print(email)


