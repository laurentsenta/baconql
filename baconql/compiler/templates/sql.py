from sqlalchemy import text
from sqlalchemy.types import * {# TODO: maybe use explicit imports? #}

{# TODO: read some documentation about jinja whitespacing & clean these `{%-' everywhere #}

{% for block in blocks %}
def {{ block.name }}(
    {%- for arg in block.all_inputs('db') %}
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

    r = db.execute(stmnt
            {# Parameters defined in the SQL header (with typing information): #}
            {%- if block.input_args -%},
                {%- for arg in block.input_args %}
                    {{- arg.name }}={{ arg.name }}{% if not loop.last %}, {% endif %}
                {%- endfor %}
            {% endif %}
            {# Parameters extracted from the SQL body: #}
            {% if block.input_implicits_names -%},
                {%- for arg in block.input_implicits_names %}
                    {{- arg }}={{ arg }}{% if not loop.last %}, {% endif %}
                {%- endfor %}
            {% endif %}
    )

    {% with exec_sym = 'r', dest_sym = 'd', prefix = '    ' %}
    {%- include block.result_template %}
    {% endwith -%}

    return d
{% endfor %}