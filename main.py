from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from contextlib import asynccontextmanager

from database import init_db
from resolvers import resolvers

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("API siap! Akses GraphiQL di http://localhost:8000/graphql")
    yield

app = FastAPI(
    title="Star Wars GraphQL API",
    lifespan=lifespan
)

# Load schema and start GraphQL server
type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, resolvers)
graphql_app = GraphQL(schema, debug=True)

# Mount endpoint GraphQL
app.mount("/graphql", graphql_app)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Selamat datang di Star Wars GraphQL API! Buka /graphql untuk mulai."}