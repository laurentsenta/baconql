import logging

from jinja2 import Environment, PackageLoader

log = logging.getLogger(__name__)

__ENV = Environment(loader=PackageLoader('baconql.compiler', 'templates'), extensions=['jinja2.ext.with_'])


def render(output, blocks):
    template = __ENV.get_template('sql.py')

    rendered = template.render(blocks=blocks)

    log.info("rendering to: %s", output)

    with open(output, 'w') as f:
        f.write(rendered)

    log.info("rendering of %s complete", output)
