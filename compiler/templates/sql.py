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

    return r.scalar()

{% endfor %}