#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXTURE_SHADER

uniform sampler2D texture;
uniform vec2 texOffset;

varying vec4 vertColor;
varying vec4 vertTexCoord;

const vec4 lumcoeff = vec4(0.299, 0.587, 0.114, 0);

void main() {
  vec2 tc0 = vertTexCoord.st + vec2(-texOffset.s, -texOffset.t);
  vec2 tc1 = vertTexCoord.st + vec2(         0.0, -texOffset.t);
  vec2 tc2 = vertTexCoord.st + vec2(-texOffset.s,          0.0);
  vec2 tc3 = vertTexCoord.st + vec2(+texOffset.s,          0.0);
  vec2 tc4 = vertTexCoord.st + vec2(         0.0, +texOffset.t);
  vec2 tc5 = vertTexCoord.st + vec2(+texOffset.s, +texOffset.t);

  vec4 col0 = texture2D(texture, tc0);
  vec4 col1 = texture2D(texture, tc1);
  vec4 col2 = texture2D(texture, tc2);
  vec4 col3 = texture2D(texture, tc3);
  vec4 col4 = texture2D(texture, tc4);
  vec4 col5 = texture2D(texture, tc5);

  vec4 sum = vec4(0.5) + (col0 + col1 + col2) - (col3 + col4 + col5);
  float lum = dot(sum, lumcoeff);
  gl_FragColor = vec4(lum, lum, lum, 1.0) * vertColor;
}