from flask import Flask, redirect, url_for, session, request, render_template
from authlib.integrations.flask_client import OAuth
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    client_kwargs={
        "scope": "openid profile email",
    },
)


def get_management_token():
    url = f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token"

    payload = {
        "client_id": os.getenv("AUTH0_M2M_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_M2M_CLIENT_SECRET"),
        "audience": f"https://{os.getenv('AUTH0_DOMAIN')}/api/v2/",
        "grant_type": "client_credentials",
    }

    response = requests.post(url, json=payload)
    return response.json()["access_token"]


def update_user_metadata(user_id, data):
    token = get_management_token()

    url = f"https://{os.getenv('AUTH0_DOMAIN')}/api/v2/users/{user_id}"

    headers = {"authorization": f"Bearer {token}", "content-type": "application/json"}

    body = {"user_metadata": data}

    requests.patch(url, json=body, headers=headers)


def get_user_full(user_id):
    token = get_management_token()

    url = f"https://{os.getenv('AUTH0_DOMAIN')}/api/v2/users/{user_id}"

    headers = {"authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/")
def home():
    user = session.get("user")

    if user:
        return f"""
        <h1>Bienvenido {user['name']}</h1>
        <a href="/profile">Editar datos</a><br>
        <a href="/logout">Cerrar sesión</a>
        """

    return '<a href="/login">Login</a>'


@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri="http://localhost:5000/callback")


@app.route("/callback")
def callback():
    token = auth0.authorize_access_token()
    user = token.get("userinfo")

    # 🔥 obtener datos completos desde Auth0
    full_user = get_user_full(user["sub"])

    session["user"] = full_user

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout"
        f"?returnTo=http://localhost:5000"
        f"&client_id={os.getenv('AUTH0_CLIENT_ID')}"
    )


@app.route("/profile")
def profile():
    user = session.get("user")

    if not user:
        return redirect("/")

    return render_template("profile.html", user=user)


@app.route("/update", methods=["POST"])
def update():
    user = session.get("user")

    if not user:
        return redirect("/")

    user_id = user.get("user_id") or user.get("sub")

    data = {
        "tipo_doc": request.form.get("tipo_doc"),
        "num_doc": request.form.get("num_doc"),
        "direccion": request.form.get("direccion"),
        "telefono": request.form.get("telefono"),
    }

    update_user_metadata(user_id, data)

    return """
    <h3>Datos guardados correctamente ✅</h3>
    <a href="/profile">Volver al perfil</a>
    """


app.run(debug=True)
