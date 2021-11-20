import math


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def squared_length(self):
        return self.x*self.x + self.y*self.y + self.z*self.z

    @property
    def length(self):
        return math.sqrt(self.squared_length)

    @property
    def squared_horizontal_length(self):
        return self.x*self.x + self.z*self.z

    @property
    def horizontal_length(self):
        return math.sqrt(self.squared_horizontal_length)

    def __add__(self, o):
        return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)

    # pairwise multiplication
    def __mul__(self, o):
        return Vec3(self.x * o.x, self.y * o.y, self.z * o.z)


class ElytraEmulator:
    def __init__(self, start_pitch=0, start_yaw=0, start_position=Vec3(0, 0, 0), start_velocity=Vec3(0, 0, 0)):
        self.pitch = start_pitch
        self.yaw = start_yaw
        self.position = start_position
        self.velocity = start_velocity

    @property
    def speed(self):
        return self.velocity.length

    @property
    def rotation_vector(self):
        f = self.pitch * (math.pi / 180)
        g = -self.yaw * (math.pi / 180)
        h = math.cos(g)
        i = math.sin(g)
        j = math.cos(f)
        k = math.sin(f)
        return Vec3(i * j, -k, h * j)

    def tick(self):
        # emulate maximum speed threshold on multiplayer server
        if self.speed > 1.65:
            self.velocity = Vec3(0, 0, 0)

        d = 0.08
        vec3d5 = self.velocity
        vec3d6 = self.rotation_vector
        j = self.pitch * (math.pi / 180)
        k = vec3d6.horizontal_length
        l = vec3d5.horizontal_length
        m = vec3d6.length
        n = math.cos(j)
        n = (n * (n * min(1.0, m / 0.4)))
        vec3d5 = self.velocity + Vec3(0.0, d * (-1.0 + n * 0.75), 0.0)
        if vec3d5.y < 0.0 and k > 0.0:
            o = vec3d5.y * -0.1 * n
            vec3d5 = vec3d5 + Vec3(vec3d6.x * o / k, o, vec3d6.z * o / k)

        if j < 0.0 and k > 0.0:
            p = l * (-math.sin(j)) * 0.04
            vec3d5 = vec3d5 + Vec3(-vec3d6.x * p / k, p * 3.2, -vec3d6.z * p / k)

        if k > 0.0:
            vec3d5 = vec3d5 + Vec3((vec3d6.x / k * l - vec3d5.x) * 0.1, 0.0, (vec3d6.z / k * l - vec3d5.z) * 0.1)

        self.velocity = vec3d5 * Vec3(0.99, 0.98, 0.99)
        self.position += self.velocity
