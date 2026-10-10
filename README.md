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
│   │  
│   ├───model
│   │      delay_prediction.py
│   │      delay_prediction_db.py
│   │      fare_prediction.py
│   │      fare_prediction_db.py
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
    │   airlines.json
    │   airports.json
    │   eslint.config.js
    │   index.html
    │   package-lock.json
    │   package.json
    │   README.md
    │   USA_airports.json
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

The prediction APIs use local SQLite databases during local development. For Vercel, configure `DATABASE_URL` with your Supabase Postgres connection string; the backend requires it in Vercel rather than writing prediction history to ephemeral function storage. In Supabase, copy a database connection string from **Project Settings → Database → Connection string**. Use the pooler connection string for serverless deployments, and add it to the Vercel project's **Settings → Environment Variables** as `DATABASE_URL` for every environment where the app is deployed. Redeploy after changing the variable.

Keep `DATABASE_URL` server-side only: do not use a `VITE_` prefix or expose it in frontend code. The backend creates the `fare_prediction` and `delay_prediction` tables from its SQLAlchemy models when it connects. Prediction history is then stored in Supabase Postgres rather than local files.

The backend pins `xgboost-cpu` rather than the standard `xgboost` distribution. The delay classifier runs on CPU, and the CPU-only distribution avoids XGBoost's large Linux NCCL dependency, which can exceed Vercel's function bundle-size limit.

### Database
For local development without `DATABASE_URL`, the prediction APIs create `fare_prediction.db` and `delay_prediction.db` in the backend folder. To use Supabase locally, set `DATABASE_URL` in the backend process environment before starting Uvicorn. You can inspect Supabase prediction history in the Supabase SQL Editor by querying the `fare_prediction` and `delay_prediction` tables.
