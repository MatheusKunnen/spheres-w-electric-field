
class VectorUtils:
    def __init__(self):
        pass

    @staticmethod
    def norm_2(vec):
        return vec[0]**2 + vec[1]**2 + vec[2]**2

    @staticmethod
    def norm(vec):
        return VectorUtils.norm_2(vec)**(1./2)

    