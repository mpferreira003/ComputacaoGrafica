#version 330 core

in vec2 out_texture;
in vec3 out_normal;
in vec3 out_fragPos;

out vec4 fragColor;

// Estrutura para as luzes
struct Light {
    vec3 position;
    vec3 color;
    float ambient;
    float diffuse;
    float specular;
    bool enabled;
    bool isOutdoor;  // Se true, afeta apenas objetos outdoor
};

// Número máximo de luzes
#define MAX_LIGHTS 10

// Uniformes
uniform sampler2D texture_diffuse1;
uniform vec3 viewPos;
uniform bool isOutdoor;
uniform vec3 ambientLight;
uniform float ambientIntensity;

// Propriedades do material
uniform float ka;    // Coeficiente ambiente
uniform float kd;    // Coeficiente difuso
uniform float ks;    // Coeficiente especular
uniform float ns;    // Expoente especular

// Array de luzes
uniform Light lights[MAX_LIGHTS];
uniform int numLights;

// Função para calcular a contribuição de uma luz
vec3 calculateLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir, vec3 texColor, bool fragmentIsOutdoor) {
    if (!light.enabled) return vec3(0.0);
    
    // Verifica se a luz deve afetar este fragmento
    // - Se a luz for outdoor, só afeta fragmentos outdoor (fragmentIsOutdoor = true)
    // - Se a luz for indoor, só afeta fragmentos indoor (fragmentIsOutdoor = false)
    if (light.isOutdoor != fragmentIsOutdoor) {
        return vec3(0.0);
    }
    
    // Direção da luz
    vec3 lightDir = normalize(light.position - fragPos);
    
    // Componente difusa
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = light.diffuse * diff * light.color * kd;
    
    // Componente especular
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
    vec3 specular = light.specular * spec * light.color * ks;
    
    // Atenuação
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (1.0 + 0.1 * distance + 0.01 * (distance * distance));
    
    // Aplica atenuação
    diffuse *= attenuation;
    specular *= attenuation;
    
    // Retorna a contribuição total da luz
    return (diffuse + specular) * texColor;
}

void main() {
    // Cor da textura
    vec4 textureColor = texture(texture_diffuse1, out_texture);
    
    // Normal do fragmento e direção de visualização
    vec3 norm = normalize(out_normal);
    vec3 viewDir = normalize(viewPos - out_fragPos);
    
    // Aplica a luz ambiente
    vec3 ambient = ambientLight * ambientIntensity * ka * textureColor.rgb;
    vec3 result = ambient;
    
    // Aplica todas as luzes
    for (int i = 0; i < numLights; i++) {
        result += calculateLight(lights[i], norm, out_fragPos, viewDir, textureColor.rgb, isOutdoor);
    }
    
    // Garante que os valores de cor estejam no intervalo [0, 1]
    result = clamp(result, 0.0, 1.0);
    
    // Define a cor final do fragmento
    fragColor = vec4(result, textureColor.a);
}