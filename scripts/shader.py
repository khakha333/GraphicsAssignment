from pyglet.graphics.shader import Shader, ShaderProgram

# 단색용
vertex_source_default = """
#version 330
layout(location = 0) in vec3 vertices;
layout(location = 1) in vec4 colors;

out vec4 newColor;

uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0);
    newColor = colors;
}
"""

fragment_source_default = """
#version 330
in vec4 newColor;
out vec4 outColor;

void main()
{
    outColor = newColor;
}
"""

# 텍스처용
vertex_source_tex = """
#version 330
layout(location = 0) in vec3 vertices;
layout(location = 1) in vec2 texCoords;

out vec2 vTexCoord;

uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0);
    vTexCoord = texCoords;
}
"""

fragment_source_tex = """
#version 330
in vec2 vTexCoord;
out vec4 outColor;

uniform sampler2D myTexture;

void main()
{
    outColor = texture(myTexture, vTexCoord);
}
"""

def create_program(vs_source, fs_source):
    vert_shader = Shader(vs_source, 'vertex')
    frag_shader = Shader(fs_source, 'fragment')
    return ShaderProgram(vert_shader, frag_shader)
