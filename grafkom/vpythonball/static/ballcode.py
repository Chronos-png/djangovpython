from vpython import *
import random
# scene = canvas(title = "220411100130", size= 20, center=vector(0, 0, 0))

class tagrafkom:
    box_size = 20
    scene = canvas(title = "220411100130", size= box_size, center=vector(0, 0, 0))
    balls = None

    def __init__(self):
        self.balls = self.makeBall(5, self.box_size, 2)
        self.balls = self.coloring_ball(self.balls)

        scene.bind('keydown',self.Keyboard)

        while True:
            rate(24)
            for i in range(len(self.balls)):
                if i != 0:
                    self.balls[i].pos += (self.balls[i].velocity * 2)
                if abs(self.balls[i].pos.x) >= self.box_size:
                    self.balls[i].velocity.x *= -1
                if abs(self.balls[i].pos.y) >= self.box_size:
                   self.balls[i].velocity.y *= -1
                # Hit DeadlyBall Condition
                # dead_trigger(balls[i], balls[0], i)
                # Cek Collision
                for j in range(i + 1, len(self.balls)):
                    self.check_collision(self.balls[i], self.balls[j], i)
                
                # if balls[i].state == "die":
                #     balls[i].pos.z = -balls[i].radius*2
                #     balls[i].color = color.white
                
            # label(text = f"Kill = {balls[0].kill}")

    def makeBall(self, jumlahBola, box_size, ball_radius):
        result = []
        for ball in range(jumlahBola):
            if ball>0 :
                random_position = None
                for ball_position in result:
                    while random_position == None or mag(ball_position.pos - random_position) <= ball_radius*2:                             
                        random_position = vector(random.uniform(-box_size, box_size), random.uniform(-box_size, box_size), 0)
            else:
                random_position = vector(random.uniform(-box_size, box_size), random.uniform(-box_size, box_size), 0)
            result.append(sphere(pos=random_position, radius = ball_radius, velocity = vector(0.1, 0.1, 0), state="alive", kill = 0))
        return result
    
    def coloring_ball(self, ball_vault):
        for i in range(len(ball_vault)):
            color = vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
            color = self.check_color_existence(ball_vault, color)
            ball_vault[i].color = color
            if i == 0:
                ball_vault[i].color = vector(200, 0 , 255)
                ball_vault[i].velocity = vector(0, 0, 0)
        return ball_vault

    def check_color_existence(self, ball_vault, color):
        for ball in ball_vault:
            while color == ball.color:
                color = vector(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return color
    
    def check_collision(self, ball1, ball2, iteration):
        dist = mag(ball1.pos - ball2.pos)
        if dist <= ball1.radius + ball2.radius:
            # Calculate new velocities after collision
            v1 = ball1.velocity
            v2 = ball2.velocity
            m1 = ball1.radius**3
            m2 = ball2.radius**3
            new_v1 = v1 - 2 * m2 / (m1 + m2) * dot(v1 - v2, ball1.pos - ball2.pos) / mag(ball1.pos - ball2.pos)**2 * (ball1.pos - ball2.pos)
            new_v2 = v2 - 2 * m1 / (m1 + m2) * dot(v2 - v1, ball2.pos - ball1.pos) / mag(ball2.pos - ball1.pos)**2 * (ball2.pos - ball1.pos)
            if ball1.state == "alive" and ball2.state == "alive": #Check if its still alive
                if iteration == 0:
                    ball2.velocity *= -1
                    return None
                ball1.velocity = new_v1
                ball2.velocity = new_v2
    
    def dead_trigger(self, current_ball, deadly_ball, iteration):
        if iteration == 0:
            return None
        if mag(current_ball.pos - deadly_ball.pos) <= (current_ball.radius*2) + 0.1:
            current_ball.velocity = vector(0, 0, 0)
            if current_ball.state == "alive":
                deadly_ball.kill += 1
            current_ball.state = "die"
    
    def Keyboard(self, key_event):
        key = key_event.key
        speed = 0.1 * 7.25
        # Move the ball based on the arrow keys
        if key == 'up':
            self.balls[0].pos.y += speed
        if key == 'down':
            self.balls[0].pos.y -= speed
        if key == 'right':
            self.balls[0].pos.x += speed
        if key == 'left':
            self.balls[0].pos.x -= speed