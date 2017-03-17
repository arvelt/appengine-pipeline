# -*- coding: utf-8 -*-
import logging
import pipeline
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return """
    <li><a href="/test-deferred"/>/test-deferred</li>
    <li><a href="/pypeline-sync">/pypeline-sync</li>
    <li><a href="/pypeline-multiple-tasks">/pypeline-multiple-tasks</li>
    """


def do_something_expensive(a, b, c=None):
    logging.info("Doing something expensive! %r %r %r", a, b, c)


@app.route("/test-deferred")
def test_deferred():
    u"""Use deferred."""
    from google.appengine.ext import deferred
    deferred.defer(do_something_expensive, "Hello, world!", 42, c=True)
    return "See server log."


@app.route("/pypeline-sync")
def pypeline_sync():
    """Use pypeline sync."""
    square_stage = SquarePipeline(10)
    square_stage.start()
    return "See server log"


class SquarePipeline(pipeline.Pipeline):

    output_names = ['square']

    def run(self, number):
        self.fill(self.outputs.square, number * number)

    def finalized(self):
        logging.info('All done! Square is %s', self.outputs.square.value)


@app.route("/pypeline-multiple-tasks")
def pypeline_multiple_tasks():
    stage = FanOutFanInPipeline(10)
    stage.start()
    return "See server log"


class SquarePipeline2(pipeline.Pipeline):

    def run(self, number):
        logging.info('Squaring: %s' % number)
        return number * number


class Sum(pipeline.Pipeline):

    def run(self, *args):
        value = sum(list(args))
        logging.info('Sum: %s', value)
        return value


class FanOutFanInPipeline(pipeline.Pipeline):

    def run(self, count):
        results = []
        for i in xrange(0, count):
            result = yield SquarePipeline2(i)
            results.append(result)

        yield Sum(*results)


if __name__ == "__main__":
    app.run()
