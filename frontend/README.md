# Flightforesight (Frontend)

## Installation

**Important Note**: Ensure that the terminal directory is strictly navigated to the right directory of `./COS30049-COMPUTING-TECHNOLOGY-INNOVATION-PROJECT_FLIGHTFORESIGHT/flightforesight` 

Run the following command to install all the required dependencies

```
npm install
```

## Supabase datasets

The fare prediction form reads all rows from the `airlines` and `airports`
tables in Supabase. The delay prediction form reads all rows from `USA_airports`;
that table must include `iata`, `name`, `latitude`, and `longitude` columns so
the form can select airports and calculate route distance. All tables must be
readable with the configured publishable key; for public access, configure
appropriate `SELECT` policies in Supabase Row Level Security.

For local development, create `frontend/.env.local` with the Supabase project
URL and publishable key:

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your-publishable-key
```

In Vercel, add `VITE_SUPABASE_URL` and `VITE_SUPABASE_PUBLISHABLE_KEY` under
the frontend project's Environment Variables, then redeploy. Restart the Vite
development server after changing local environment variables. The app itself
still loads without these settings, but the fare and delay forms will show a
configuration error until they are set.

## Running

### Flightforesight (frontend)

**Important Note**: Ensure that the terminal directory is strictly navigated to the right directory of `./COS30049-COMPUTING-TECHNOLOGY-INNOVATION-PROJECT_FLIGHTFORESIGHT/flightforesight` 

To start the localhost server hosting the website frontend, run the following command

```
npm run dev
```

If successful, the server should be accessible at:

```
http://localhost:5173/
```

This URL will open the React application in your web browser, allowing you to interact with the frontend.
