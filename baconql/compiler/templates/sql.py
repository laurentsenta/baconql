from sqlalchemy import text
from sqlalchemy.types import * {# TODO: maybe use explicit imports? #}

{# TODO: read some documentation about jinja whitespacing & clean these `{%-' everywhere #}

{% for block in blocks %}
def {{ block.name }}(
    {%- for arg in block.input_names('db') %}
        {{- arg }}{% if not loop.last %},{% endif %}
    {%- endfor %}):
    {%- if block.docs %}
    """
    {%- for doc in block.docs %}
    {{ doc.value -}}
    {% endfor %}
    """
    {%- endif %}

    stmnt = text("""
        {{ block.statement('        ') }}
    """)

    {%- if block.output_args %}
    stmnt = stmnt.columns(
            {%- for arg in block.output_args %}
              {{ arg.name }}={{ arg.value }}
            {%- endfor %}
    )
    {% endif %}

    {% if block.input_args -%}
    r = db.execute(stmnt,
                   {%- for arg in block.input_args %}
                       {{- arg.name }}={{ arg.name }}{% if not loop.last %}, {% endif %}
                   {%- endfor %})
    {% else -%}
    r = db.execute(stmnt)
    {% endif -%}

    {%- with exec_sym = 'r', dest_sym = 'd', prefix = '    ' %}
    {%- include block.result_template %}
    {% endwith -%}

    return d
{% endfor %}