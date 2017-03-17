import logging
import pipeline
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/pypeline-sync")
def get():
    square_stage = SquarePipeline(10)
    square_stage.start()
    return ""

class SquarePipeline(pipeline.Pipeline):

    output_names = ['square']

    def run(self, number):
        self.fill(self.outputs.square, number * number)

    def finalized(self):
        logging.info('All done! Square is %s', self.outputs.square.value)

if __name__ == "__main__":
    app.run()
