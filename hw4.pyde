numPoints = 150
points = []
speedMul = 1.0
maxDist = 50
WHITE = (255, 255, 255)
ORANGE = (255, 103, 0)
BLUE = (34, 188, 242)
YELLOW = (255, 230,0)
GREEN = (127, 221, 5)
colors = [WHITE, ORANGE, BLUE, YELLOW, GREEN]
colorIndicators = None
colorCode = {
    WHITE: 0,
    ORANGE: 1,
    BLUE: 2,
    YELLOW: 3,
    GREEN: 4
}
currColor = 1

def setup():
    global points, colorIndicators
    size(800, 600)
    for i in range(numPoints):
        points.append(Point(random(width), random(height), WHITE))  # initial white color
    colorIndicators = [Point(380, 20, colors[0]), Point(400, 20, colors[1]), Point(420, 20, colors[2])]
    print(map((lambda x: sum(x)), colors))

def draw():
    background(30)
    
    # draw line
    for i in range(numPoints):
        for j in range(i+1, len(points)):
            d = dist(points[i].x, points[i].y, points[j].x, points[j].y)
            if d < maxDist:
                alpha = map(d, 0, maxDist, 255, 0)
                stroke(255, alpha)
                line(points[i].x, points[i].y, points[j].x, points[j].y)
    
    # color change
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if (points[i].color != points[j].color):
                d = dist(points[i].x, points[i].y, points[j].x, points[j].y)
                if d < 5:
                    # Change the color of both points to blue
                    newColor = colorPriority(points[i].color, points[j].color)
                    if newColor != -1:
                        points[i].color = newColor
                        points[j].color = newColor

                    
    # draw points
    for point in points:
        point.repel(mouseX, mouseY)
        point.move()
        point.display()
    
    # draw indicator
    colorIndicators[0].color = colors[(currColor - 1) % len(colors)]
    colorIndicators[0].display(10)
    colorIndicators[1].color = colors[currColor]
    colorIndicators[1].display(20)
    colorIndicators[2].color = colors[(currColor + 1) % len(colors)]
    colorIndicators[2].display(10)
        
def colorPriority(c1, c2):
    diff = colorCode[c1] - colorCode[c2]
    if diff == 1 or diff == -4:
        return c1
    if diff == -1 or diff == 4:
        return c2
    return -1
        
def keyPressed():
    global speedMul, points, colors, currColor
    # change simulation speed
    if keyCode == UP:
        speedMul += 0.1
    elif keyCode == DOWN:
        speedMul -= 0.1
        speedMul = max(0, speedMul)
    # cycle through color
    elif keyCode == LEFT:
        currColor = (currColor - 1) % len(colors)
    elif keyCode == RIGHT:
        currColor = (currColor + 1) % len(colors)
    # spawn new points
    elif key == ' ':
        points.append(Point(mouseX, mouseY, colors[currColor]))  # light blue color


class Point:
    def __init__(self, x, y, color=WHITE):
        self.x = x
        self.y = y
        self.color = color
        self.speedX = random(-2, 2) * speedMul
        self.speedY = random(-2, 2) * speedMul
        
    def move(self):
        self.x += self.speedX * speedMul
        self.y += self.speedY * speedMul
        if self.x > width: 
            self.x = 0
        if self.x < 0: 
            self.x = width
        if self.y > height: 
            self.y = 0
        if self.y < 0: 
            self.y = height
            
    def repel(self, mx, my):
        d = dist(self.x, self.y, mx, my)
        if d < 100:
            force = 1.0 + (100 - d) * 0.1
            angle = atan2(self.y - my, self.x - mx)
            self.speedX = force * cos(angle) * speedMul
            self.speedY = force * sin(angle) * speedMul
            
    def display(self, r=5):
        fill(self.color[0], self.color[1], self.color[2])
        noStroke()
        ellipse(self.x, self.y, r, r)
    
