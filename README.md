# COS30049 - Computing Technology Innovation Project (CAA Flightforesight)

## File structure

The project folder is organized into two main subfolders: backend and flightforesight (frontend).

1. Backend: 
    - The `backend` folder is further divided into two main subfolders: `model` and `preprocessor`.
    - The `model` folder contains the backend logic for the web application, including the request processing files and three pre-trained Machine Learning models: `lgbm_regressor_delay.pkl`, `rf_regressor.pkl`, and `xgboost_tuned_model.pkl`.
    - The `preprocessor` folder has code for processing the input data received from the frontend input form.

2. flightforesight (frontend):
    - The `flightforesight` folder is structured as a standard React project, containing `src`, `public`, and `package.json`.
    - Additional files like `airlines.json`, `airports.json`, and `USA_airports.json` are included for user input validation and processing.
    - Inside the `src` folder, there are two subfolders: `assets` and `components`. The assets folder is used to store media files, such as images of team members, while the `components` folder contains the React components that form the frontend of the web application.


```
COS30049-COMPUTING-TECHNOLOGY-INNOVATION-PROJECT_FLIGHTFORESIGHT
│   .DS_Store
│   .gitignore
│   LICENSE
│   README.md
│
├───backend
│   │   .DS_Store
│   │   requirements.txt
│   │   supabase_schema.sql
│   │  
│   ├───model
│   │      delay_prediction.py
│   │      fare_prediction.py
│   │      supabase_store.py
│   │      lgbm_regressor_delay.pkl
│   │      rf_regressor.pkl
│   │      xgboost_tuned_model.pkl
│   │   
│   └───preprocessor
│           preprocessorfordelay-classify.pkl
│           preprocessorfordelays.pkl
│
└───flightforesight
    │   .gitignore
    │   eslint.config.js
    │   index.html
    │   package-lock.json
    │   package.json
    │   README.md
    │   vite.config.js
    │
    └───src
        │   App.jsx
        │   main.jsx
        │
        ├───assets
        │       Justin.jpeg
        │       Melvin.jpg
        │       MinhHoangDuong.jpg
        │
        └───components
                components.css
                Delay.jsx
                Fare.jsx
                FlightPath.jsx
                FlightTableForDelay.jsx
                FlightTableForFare.jsx
                Footer.jsx
                home.jsx
                Navbar.jsx
                ScatterPlotForDelay.jsx

```

## Installation
### Flightforesight(Frontend) 

**Important Note**: Ensure that the terminal directory is strictly navigated to the right directory of `./COS30049-COMPUTING-TECHNOLOGY-INNOVATION-PROJECT_FLIGHTFORESIGHT/flightforesight` 

Run the following command to install all the required dependencies

```
npm install
```

### Backend

**Important Note**: Ensure that the terminal directory is strictly navigated to the right directory of `./COS30049-COMPUTING-TECHNOLOGY-INNOVATION-PROJECT_FLIGHTFORESIGHT/backend` 

Run the following command to install all the required dependencies

```
pip install -r requirements.txt
```

## Running

### Flightforesight (frontend)

**Important Note**: Ensure that the terminal directory is strictly navigated to the right directory of `./COS30049-COMPUTING-TECHNOLOGY-INNOVATION-PROJECT_FLIGHTFORESIGHT/flightforesight` 

To start the localhost server hosting the website frontend, run the following command

```
npm run dev
```

If successful, the server should be accessible in localhost

This URL will open the React application in your web browser, allowing you to interact with the frontend.


### Backend

**Important Note**: A new terminal is needed to run the backend concurrently with the frontend. Make sure that this terminal is strictly in the correct directory of `./COS30049-COMPUTING-TECHNOLOGY-INNOVATION-PROJECT_FLIGHTFORESIGHT/backend` 

Start the combined backend so both prediction APIs are available to the frontend:

```
uvicorn main:app --reload --port 8000
```

The Vite development server proxies `/api` requests to this backend. The combined app serves fare routes under `/api/fare/...` and delay routes under `/api/delay/...`.

## Vercel deployment

The root `vercel.json` defines two services: `backend` (FastAPI, rooted at `backend/`) and `frontend` (Vite, rooted at `frontend/`). Requests under `/api/` route to the backend; all other paths route to the frontend.

Prediction results and history use the Supabase Data API. In Supabase, run
[`backend/supabase_schema.sql`](./backend/supabase_schema.sql) in the SQL Editor
to create the `fare_predictions` and `delay_predictions` tables. The backend
uses `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`; configure both as
server-side environment variables in Vercel and redeploy. For local development,
set these variables in the backend process environment before starting Uvicorn.
Never use a `VITE_` prefix or expose the service-role key to the frontend.

The backend pins `xgboost-cpu` rather than the standard `xgboost` distribution. The delay classifier runs on CPU, and the CPU-only distribution avoids XGBoost's large Linux NCCL dependency, which can exceed Vercel's function bundle-size limit.

The delay regressor is served as ONNX so the Vercel runtime does not need LightGBM's Linux `libgomp.so.1` library. To regenerate the ONNX artifact after replacing the original trained model, install the conversion-only dependencies and run the exporter from the backend directory:

```
pip install -r requirements-conversion.txt
python export_delay_model.py
```

### Prediction history
Prediction history is stored in the `fare_predictions` and `delay_predictions`
Supabase tables. The history endpoints read these tables through the Supabase
Data API. The SQL Editor can also be used to inspect the saved records.
