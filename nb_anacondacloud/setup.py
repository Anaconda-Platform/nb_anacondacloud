from os.path import join, abspath, dirname
from nbsetuptools import setup


setup(
    name="nb_anacondacloud",
    version="0.2.0",
    static=join(abspath(dirname(__file__)), 'static')
)
