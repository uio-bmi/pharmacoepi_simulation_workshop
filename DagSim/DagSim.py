from dagsim.utils.parser import DagSimSpec

parser = DagSimSpec("definition.yaml")

data = parser.parse(draw=True)
