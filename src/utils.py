from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.routing import APIRoute

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
    
def generate_sitemap(app: FastAPI):
    links = [{ "method": 'GET', "url": '/admin/', "params": None }]

    for route in app.routes:
        if isinstance(route, APIRoute):
            for method in route.methods:
                url = route.path
                links.append({ "method": method, "url": url, "params": route.dependant.path_params })

    links_html = ""
    for r in links:
        if r['params'] or r['method'] != "GET": links_html += f"<li>{r['method']} {r['url']}</li>"
        else: links_html += f"<li><a href='{r['url']}'>{r['method']} {r['url']}</a></li>"

    return f"""
        <div style="text-align: center;">
            <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
            <h1>Rigo welcomes you to your API!!</h1>
            <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
            <p>Start working on your project by following the <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a></p>
            <p>Remember to specify a real endpoint path like: </p>
            <ul style="text-align: left;">{links_html}</ul>
        </div>
    """

def bootstrap_app(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Disable strict slashes
    for route in app.router.routes:
        if isinstance(route, APIRoute):
            route.strict_slashes = False


    @app.exception_handler(APIException)
    def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )
    
    @app.get("/")
    def read_root(request: Request):
        return HTMLResponse(generate_sitemap(app))

    return app