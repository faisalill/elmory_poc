# Getting Started

## Running and Building the Frontend

Move to the frontend directory and install packages.

sh```
cd frontend && npm install

```

Build and static export the frontend

sh```
npm run build

```

> This will create a build folder which contains the statically exported js, html and css files.

## Setting up and Running the Server

Move to the backend directory and install dependencies

sh```
cd backend && pip install -r requirements.txt

```

Start the server

sh```
uvicorn server:app

```

> The app should be running go to localhost:8000/getfacl.html
