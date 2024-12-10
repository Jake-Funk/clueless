# Clueless

This is our implementation of Clue for the Foundations of Software Engineering class at JHU's EP program.

The frontend is built using Next.js, the backend is built using FastAPI.

## Prerequisites

### Server
- This project was developed and implemented on Unix based systems such as Mac and Linux, so using another operating system might not work
- You will need to setup your python environment for the FastAPI's server with Astral's `uv`. Found here: [https://docs.astral.sh/uv/getting-started/]
- Once you have `uv` setup, you can install packages from the main repo (clueless/server). You have to run all commands prefaced with `uv`
  - `uv install` for downloading packages
  - `uv run` for most normal commands such as `uv run python file_name.py`
- To start the server in production mode run (in the `clueless/server` folder) `uv run fastapi dev main.py`
  - By default this will start the server on [localhost:8000]
  - To see FastAPI's documentation for the server go to: [http://localhost:8000/docs]

### Client
- You will need to set up `npm`. Docs are found here: [https://docs.npmjs.com/downloading-and-installing-node-js-and-npm]
- To start the development server you can run `npm run dev` in `clueless/client/clueless_web_ui`
  - Open your browser to [http://localhost:3000] to see the results
- To connect with your local Server
  - You will need a `.env.local` file in `clueless/client/cluess_web_ui`
  - In that file you will need to point to your local server with: `NEXT_PUBLIC_SERVER_URL=http://localhost:8000`
