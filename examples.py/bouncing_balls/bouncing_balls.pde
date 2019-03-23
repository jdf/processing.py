# n0vice.hasi
Ball[] balls = new Ball[5];

void setup(){
  size(640,380);
  for (int i = 0; i < balls.length; i++){
    balls[i] = new Ball();
  }
}



void draw(){
  background(250);
  stroke(0);
  strokeWeight(2);
  fill(128);
  for (int i = 0; i < balls.length; i++){
    balls[i].physics();
    balls[i].show();
  }
  
  
}
