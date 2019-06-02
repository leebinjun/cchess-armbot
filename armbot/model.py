# 运动模型解算

import math

def model_pre(x, y):
    x, y = x-4, y-0  #相对机械臂原点坐标
    x, y = 20*x-5, 20*y+125
    dl = math.sqrt(x**2 + y**2)-60
    theta = math.atan2(x, y)*180/math.pi
    print('theta:', theta)
    print('x', (dl+60) * math.sin(math.radians(theta)))
    return dl, theta

def model_solve(dl, dh = 0):
    # input:  dl, dh
    # output: theta1, theta2 (degree of angle)
    '''
    if dl < 180:
        alpha = 90
        dl = dl - 20
    else:
        alpha = 60
        dl = dl - 22
        dh = dh - 10 
    '''
    dl = -dl
    # theta1, theta2 = f(dh, dl)
    l1 = 150
    l2 = 160
    
    A = (l1**2 + dh**2 + dl**2 - l2**2) / (2*l1)
    
    a = dl**2 + dh**2
    b = -2 * A * dl
    c = A**2 - dh**2
    
    delta = b**2 - 4*a*c
    print("b*b - 4*a*c:", delta )

    if abs(delta) < 0.01 or dh == 0:
        delta = 0
    # 当dh = 0时, datel=0，得到唯一解避免分类讨论的情况
    if delta < 0:
        print("1.No solve")
        return None
    ans1 = (-b+math.sqrt(delta))/2/a
    ans2 = (-b-math.sqrt(delta))/2/a
    print("-_val, +_val", ans1, ans2)
  
    # 分类讨论
    # TODO：@libing 看着公式很多，math.radians(theta1_d)*180/math.pi可以简化
    # 1
    theta1_d = math.acos(ans1)*180/math.pi
    theta2_d = 180 - math.asin((dh-l1*math.sin(math.radians(theta1_d)))/l2)*180/math.pi
    dl_c = l1*math.cos(math.radians(theta1_d)) + l2*math.cos(math.radians(theta2_d))
    dh_c = l2*math.sin(math.radians(theta2_d)) + l1*math.sin(math.radians(theta1_d))
    print("theta1_d, theta2_d, dl, dh", theta1_d, theta2_d, dl_c, dh_c)
    if (dl_c-dl)**2 + (dh_c - dh)**2 > 1:
        print("bad ans.")
    else:
        return theta1_d, theta2_d
    
    # 2
    theta1_d = math.acos(ans2)*180/math.pi
    theta2_d = 180 - math.asin((dh-l1*math.sin(math.radians(theta1_d)))/l2)*180/math.pi
    dl_c = l1*math.cos(math.radians(theta1_d)) + l2*math.cos(math.radians(theta2_d))
    dh_c = l2*math.sin(math.radians(theta2_d)) + l1*math.sin(math.radians(theta1_d))
    print("theta1_d, theta2_d, dl, dh", theta1_d, theta2_d, dl_c, dh_c)
    if (dl_c-dl)**2 + (dh_c - dh)**2 > 1:
        print("no ans.")
    else:
        return theta1_d, theta2_d
    
    return 0,0


    


if __name__ == "__main__":
        
    # dh, dl, alpha = -80, 180, 60
    # print(model_solve(dl, dh, alpha))
    # adict = {1:500, 2:500, 3:500, 4:500, 5:500, 6:500}
    # theta3, theta4, theta5 = model_solve(dl, dh, alpha)
    # adict[3], adict[4], adict[5] = int(500-theta3*100/24), int(500+theta4*100/24), int(500-theta5*100/24)
    # print(adict)
    # servos_to_pos(adict)


    dl = 65
    print(model_solve(dl))

    temp_a = 0
    while(temp_a != 99):
        temp_a = int(input('input the action:'))
        # dl = temp_a
        # t1, t2 = model_solve(dl)
        # ans1 = 1400 - (t1-90)*100/9
        # ans2 = 1500 + (t2-180)*100/9
        # print("t1, t2:", t1, t2)
        # print("a1, a2:", ans1, ans2)
        if temp_a == 7:
            input_x = int(input('input the x:'))
            input_y = int(input('input the y:'))
            input_z = int(input('input the z:'))
            dl, t = model_pre(input_x, input_y)
            model_solve(dl ,dh = input_z)
