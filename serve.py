from functools import wraps
from flask import Flask, request, jsonify, render_template
from graphql import graphql_sync, build_schema

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

schema = build_schema("""
    type Query {
        hello: String
        echo(msg: String!): String
    }

    type Mutation {
        shout(msg: String!): String
    }
""")

query_type = schema.get_type("Query")
mutation_type = schema.get_type("Mutation")


def resolver(root_type: str):
    def decorator(func):
        @wraps(func)
        def wrapper(obj, info, **kwargs):
            return func(obj, info, **kwargs)

        field_name = func.__name__
        if root_type == "query":
            field = query_type.fields[field_name].resolve = wrapper
        elif root_type == "mutation":
            field = mutation_type.fields[field_name].resolve = wrapper
        else:
            raise Exception("missing field")

    return decorator



@resolver('query')
def hello(obj, info):
    return "world"


@resolver('query')
def echo(obj, info, msg):
    return f"Echo: {msg}"


@resolver('mutation')
def shout(obj, info, msg):
    return msg.upper()


@app.post("/graphql")
def graphql_server():
    data = request.get_json(force=True)
    query = data.get("query")
    variables = data.get("variables")
    operation_name = data.get("operationName")

    result = graphql_sync(
        schema,
        query,
        variable_values=variables,
        operation_name=operation_name,
    )

    response = {}
    if result.errors:
        response["errors"] = [str(e) for e in result.errors]
    if result.data:
        response["data"] = result.data
    return jsonify(response)


@app.get("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
