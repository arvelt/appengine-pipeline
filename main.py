import logging
import pipeline
from google.appengine.ext import deferred
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return """
    <li><a href="/test-deferred"/>/test-deferred</li>
    <li><a href="/pypeline-sync">/pypeline-sync</li>
    """

def do_something_expensive(a, b, c=None):
    logging.info("Doing something expensive! %r %r %r", a, b, c)

@app.route("/test-deferred")
def test_deferred():
    deferred.defer(do_something_expensive, "Hello, world!", 42, c=True)
    return "See server log."

@app.route("/pypeline-sync")
def pypeline_sync():
    square_stage = SquarePipeline(10)
    square_stage.start()
    return "See server log"

class SquarePipeline(pipeline.Pipeline):

    output_names = ['square']

    def run(self, number):
        self.fill(self.outputs.square, number * number)

    def finalized(self):
        logging.info('All done! Square is %s', self.outputs.square.value)

if __name__ == "__main__":
    app.run()
