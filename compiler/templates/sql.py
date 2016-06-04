from sqlalchemy import text

{% for block in blocks %}
def {{ block.name }}(
    {%- for arg in block.args_template('db') %}
        {{- arg.name }}{% if not loop.last %},{% endif %}
    {%- endfor %}):
    stmnt = text("""
        {{ block.statement('        ') }}
    """)

    {% if block.args -%}
    r = db.execute(stmnt,
                   {%- for arg in block.args %}
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