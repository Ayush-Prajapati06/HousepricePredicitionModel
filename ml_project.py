from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import Response
from typing import Optional
from jinja2 import Environment, FileSystemLoader
import pandas as pd

import util

app = FastAPI()

@app.get('/get_location_names')
def get_location_names(request: Request):
    util.load_saved_artifacts()
    locations = util.get_location_names()
    # print('a')

    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(content={"locations":locations}, headers=headers)

@app.post('/predict_home_price')
async def predict_home_price(request: Request):
    util.load_saved_artifacts()
    form_data = await request.form()
    total_sqft = float(form_data['total_sqft'])
    location = form_data['location']
    bhk = int(form_data['bhk'])
    bath = int(form_data['bath'])

    estimated_price = util.get_estimated_price(location,total_sqft,bhk,bath)

    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(content={"predicted_price":estimated_price}, headers=headers)



if __name__=="__main__":
    print('Starting Python server for home price prediction.....')
    app.run()
