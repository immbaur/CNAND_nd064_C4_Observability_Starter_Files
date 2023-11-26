from os import getenv
import logging
import time

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask import Flask, jsonify
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter import PrometheusMetrics

from opentracing import tracer

from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory


app = Flask(__name__)
metrics = PrometheusMetrics(app)
# static information as metric
metrics.info("app_info", "Application info", version="1.0.0")

logging.getLogger("").handlers = []
logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')
print(f"JAEGER_HOST: {JAEGER_HOST}")

def init_tracer(service):

    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
            "local_agent": {"reporting_host": JAEGER_HOST}
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


tracer = init_tracer("backend")
flask_tracer = FlaskTracing(tracer, True, app)


app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)


@app.route("/")
def homepage():
    logger.info(f"API / called")

    return "Hello World"


@app.route("/api")
def my_api():
    logger.info(f"API /api called")

    parent_span = flask_tracer.get_span()
    with tracer.start_span('backend-api', child_of=parent_span) as span:
        answer = "something"
        span.set_tag("api", answer)
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    logger.info(f"API /star called")

    parent_span = flask_tracer.get_span()
    with tracer.start_span('backend-star', child_of=parent_span) as span:
        star = mongo.db.stars
        name = request.json["name"]
        distance = request.json["distance"]
        star_id = star.insert({"name": name, "distance": distance})
        new_star = star.find_one({"_id": star_id})
        output = {"name": new_star["name"], "distance": new_star["distance"]}
        span.set_tag("star", output)
    return jsonify({"result": output})

@app.route("/test")
def test():
    logger.info(f"API /test called")

    parent_span = flask_tracer.get_span()
    with tracer.start_span('backend-test', child_of=parent_span) as span:
        time.sleep(1)
        span.set_tag("test", "some test result")

    return "API /test completed"

if __name__ == "__main__":
    app.run()
