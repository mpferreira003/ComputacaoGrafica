#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texture_coord;
layout (location = 2) in vec3 normal;

out vec2 out_texture;
out vec3 out_normal;
out vec3 out_fragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
    out_texture = vec2(texture_coord);
    out_fragPos = vec3(model * vec4(position, 1.0));
    
    // Calcula a matriz normal como a transposta da inversa da submatriz 3x3 do model
    mat3 normalMatrix = transpose(inverse(mat3(model)));
    out_normal = normalize(normalMatrix * normal);
}