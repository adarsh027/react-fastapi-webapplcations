from fastapi import FastAPI, Depends, HTTPException, Request
import jwt
import snowflake.connector
#from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
#from fastapi_cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel


#import logging
#logging.basicConfig(filename="fastapi.log", level=logging.DEBUG)


app = FastAPI()

# Disable CORS by allowing all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,  # Allow credentials (e.g., cookies)
    allow_origins=["*"],  # This allows requests from all origins
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)

# # origins=['http://localhost:3000/','http://localhost:8000/']
# # # Configure CORS settings
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=[origins],  # Replace with the origin of your React app
# #     allow_credentials=True,
# #     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
# #     allow_headers=["*"],  # Allow all headers
# #     expose_headers=["*"]
# # )

# Define your custom JWT secret key (replace with your actual secret)
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"  # HMAC with SHA-256

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token_prefix, token = auth_header.split(" ")
    if token_prefix != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        # Decode the token using the custom secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        logging.info(f"Decoded JWT Token: {payload}")
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


# @app.get("/dashboard", tags=["dashboard"], response_model=str, dependencies=[Depends(get_current_user, skip_dependencies=True)])
# async def read_dashboard_data(current_user: dict = Depends(get_current_user)):
#     logging.info(f"Request received for /dashboard")
#     return f"Details for"

# @app.get("/dashboard", tags=["dashboard"], response_model=str)
# async def read_dashboard_data(request: Request):
#     # You can dynamically decide to use get_current_user or not
#     # For example, based on a condition (like a specific header)
#     if "Use-Auth" in request.headers:
#         current_user = await get_current_user(request)
#         logging.info(f"User: {current_user}")
#         # Perform actions based on current_user
#         response_data = f"Details for {current_user['sub']}"  # Use some user-specific data
#     else:
#         # If you don't want to use get_current_user
#         logging.info(f"No user authentication required")
#         response_data = "Sample API response"

#     logging.info(f"Sending response: {response_data}")
#     return response_data


class ChartData(BaseModel):
    year: int
    revenue: float

@app.get("/dashboard", response_model=List[ChartData])
async def read_dashboard_data():
    # Dummy data for testing
    dummy_data = [
        {"year": 2018, "revenue": 10000},
        {"year": 2019, "revenue": 15000},
        {"year": 2020, "revenue": 20000},
        {"year": 2021, "revenue": 25000},
        {"year": 2022, "revenue": 50000}
    ]
    return dummy_data

# @app.get("/dashboard")
# async def read_dashboard_data(current_user: dict = Depends(get_current_user)):
#     return f"Details for "
#     # Connect to Snowflake and fetch data
#     # Replace with your Snowflake connection code
