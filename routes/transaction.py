import os
import subprocess
import base64
from models.transaction import TransactionForm
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from  fastapi import Form
from database.connection import get_session
from fastapi.templating import Jinja2Templates
from config import DevConfig
import boto3
import json
import datetime


transaction_router = APIRouter(tags=["transaction"])

templates = Jinja2Templates(directory="templates/")

# Configure Boto3 to interact with the S3 service
s3_client = boto3.client('s3', region_name='us-west-2',
			aws_access_key_id=DevConfig.AWS_ID, 
			aws_secret_access_key=DevConfig.AWS_KEY
			)




def encrypt_data(data, key_file):
	"""
	Encrypt the data using OpenSSL and  a private key file.
	"""
	if isinstance(data, str):
		data = data.encode()

	# set openssl command
	cmd = [ 'openssl', 'enc', '-aes-256-cbc', '-base64', '-pass', f'file:{key_file}', '-pbkdf2']

	# Run the command with the data
	result = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if result.stderr:
		raise Exception(f"OpenSSL error: {result.stderr.decode()}")

	# Return the encrypted data
	return result.stdout.decode()


@transaction_router.post("/transaction")
async def add_transaction(
	request: Request,
	name: str = Form(...),
	email: str = Form(...),
	amount: str = Form(...),
	currency: str = Form(...),
	description: str = Form(...),
	session=Depends(get_session)
	):
	
	key = '/home/amd/derivedKey.bin'
	encrypted_name = encrypt_data(name, key)
	encrypted_email = encrypt_data(email, key)
	encrypted_amount = encrypt_data(amount, key)
	encrypted_currency = encrypt_data(currency, key)
	encrypted_description = encrypt_data(description, key)

	transaction_form = TransactionForm.as_form(
	name=encrypted_name,
	email=encrypted_email,
	amount=encrypted_amount,
	currency=encrypted_currency,
	description=encrypted_description,
	ip=request.client.host)
	print("Received contact_form:", transaction_form)
	# database goes here
	session.add(transaction_form)
	session.commit()
	session.refresh(transaction_form)

	# Convert dict to string for uploading to S3
	transaction_form_str = transaction_form.json()

	# Define the S3 bucket and object key
	bucket_name = "hsmtest1"
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	object_key = f"contact_forms/{timestamp}.json"
	# Upload the data to S3
	s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=transaction_form_str)

	return JSONResponse({"message": "success"})


