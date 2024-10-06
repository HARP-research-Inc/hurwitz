
from hurwitz import HurwitzQuaternion

q2 = HurwitzQuaternion(-1, 1, 1, 1, True)
q3 = HurwitzQuaternion(-1,0,0,0, False)

q5 = q2+q3
print(q5.decompose_binomial())

q5.debug = False
print((q5**2).decompose_binomial())
print((q5**3).decompose_binomial())
