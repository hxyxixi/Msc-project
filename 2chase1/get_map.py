
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
from mpl_toolkits.mplot3d import Axes3D
import math

# Parameters

AREA_WIDTH = 10  # potential area width [m]




def calc_potential_field(g, ox, oy, agents):

    xw = AREA_WIDTH
    yw = AREA_WIDTH
    pmap = np.zeros([xw, yw])

    for i in range(len(g)):
        pmap[g[i].x, g[i].y] = 1



    return pmap


def add_field_potential(ori_pmap, g, ox, oy, agent):
    pmap = ori_pmap.copy()
    return pmap




def draw_heatmap(data):
    data = np.array(data).T
    plt.pcolor(data, cmap=plt.cm.rainbow)
    plt.colorbar()


def obs(ox, oy): # Get no-go areas, can't appear directly next to prey
    center_x = random.randint(3, AREA_WIDTH - 3)
    center_y = random.randint(3, AREA_WIDTH - 3)
    ox.append(center_x)
    ox.append(center_x + 1)
    ox.append(center_x)
    ox.append(center_x + 1)
    oy.append(center_y)
    oy.append(center_y)
    oy.append(center_y + 1)
    oy.append(center_y + 1)


def insert_g(g, ox, oy):
    while (1):
        gx_1 = random.randint(3, AREA_WIDTH - 3)
        gy_1 = random.randint(3, AREA_WIDTH - 3)
        if in_side(ox, oy, gx_1, gy_1):
            g.append(goal(gx_1, gy_1))
            break


def in_side(a, b, c, d):
    if a == []:
        return 1
    for i in range(len(a)):
        if (abs(a[i] - c) + abs(b[i] - d)) < 3:
            return 0
    return 1


def detect(ix, iy, ox, oy):
    for j in range(len(ox)):
        if ix == ox[j] and iy == oy[j]:
            return True
    return False


def cal_dis(x1, y1, x2, y2):
    return np.hypot(x1 - x2, y1 - y2)


def get_state(pmap, ix, iy, ind, cover, agent, g):
    state = []
    s = int((cover - 1) / 2)
    for i in range(cover):
        for j in range(cover):
            try:
                state.append(pmap[max(0, ix[ind] - s + i), max(0, iy[ind] - s + j)])
            except:
                state.append(pmap.max())
    state = np.array(state).reshape(cover, cover)
    s = np.array(state).flatten()
    loc = []
    loc.append(ix[ind]/AREA_WIDTH)
    loc.append(iy[ind]/AREA_WIDTH)
    err_x = np.random.randint(-10,10)
    err_y = np.random.randint(-10,10)
    loc.append((ix[ind]-g[0].x + err_x)/AREA_WIDTH)  # add Noise
    loc.append((iy[ind]-g[0].y + err_y)/AREA_WIDTH)

    #loc.append((ix[ind]-g[0].x)/AREA_WIDTH) # no Noise
    #loc.append((iy[ind]-g[0].y)/AREA_WIDTH)

    for i in range(len(ix)):
        if i!= ind:
            loc.append((ix[i]-ix[ind])/AREA_WIDTH)
            loc.append((iy[i]-iy[ind])/AREA_WIDTH)
    
    loc = np.array(loc)
    return np.hstack([s,loc])


class goal():
    def __init__(self, x, y):
        self.range = 5
        self.time = 0
        self.send = True
        self.x = x
        self.y = y
        self.recode = []




class potential():
    def __init__(self):

        self.goals = []
        self.ox = []
        self.oy = []
        self.show_animation = False
        self.heat_show = False

        self.motion = [
            [1, 0],
            [0, 1],
            [-1, 0],
            [0, -1],
            [0, 0]]

    def insert_agent(self):
        while (1):
            ax = random.randint(1, AREA_WIDTH - 1)
            ay = random.randint(1, AREA_WIDTH - 1)
            if in_side(self.ox, self.oy, ax, ay):
                return (ax, ay)

    def insert_goal(self):
        insert_g(self.goals, self.ox, self.oy)

    def renew(self, sx, sy, agents):
        remove_list = []
        for i in range(self.agent_n):
            for j in range(len(self.goals)):
                if cal_dis(sx[i], sy[i], self.goals[j].x, self.goals[j].y) <= 1:
                    remove_list.append(j)
        for j in remove_list:
            try:
                del self.goals[j]
            except:
                print('double')


    def plot_figure(self, pmap):  #draw map
        if self.show_animation:
            plt.clf()
            #            plt.grid(True)
            #            plt.axis("equal")
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.ylim(bottom=0, top=AREA_WIDTH+2)
            plt.xlim(left=0, right=AREA_WIDTH+2)
            if self.heat_show:
                draw_heatmap(pmap)
            else:
                plt.plot(self.ox, self.oy, "*b")
                for i in range(len(self.goals)):
                    plt.plot(self.goals[i].x, self.goals[i].y, "dk") #diamond

    def reset(self, agents):
        self.agent_n = agents.n_agents
        self.ox = []
        self.oy = []
        self.goals = []
        # for i in range(agents.obs_n):
        #     obs(self.ox, self.oy)

        self.t = 0


        self.total_info = []
        self.find = 0


        for i in range(agents.n_agents):
            agents.ixs[i], agents.iys[i] = self.insert_agent()
            self.total_info.append([agents.ixs[i],agents.iys[i]])
        self.insert_goal()


        self.total_info.append(self.ox)
        self.total_info.append(self.oy)
        self.ori_pmap = calc_potential_field(self.goals, self.ox, self.oy, agents)
        self.pmap = add_field_potential(self.ori_pmap, self.goals, self.ox, self.oy, agents)
        self.plot_figure(self.pmap)
        self.rewards = 0 #initial
        self.crash = 0
        self.finish = 0
        self.dis_list = []
        for i in range(self.agent_n):
            self.dis_list.append(np.linalg.norm([agents.ixs[i] - self.goals[0].x,agents.iys[i] - self.goals[0].y]))

        self.total_action = []

        return self.pmap

    def get_avail_agent_actions(self, id):
        return [1] * 5

    def get_obs(self, agents):
        s = []
        for i in range(agents.n_agents):
            s.append(get_state(self.pmap, agents.ixs, agents.iys, i, agents.cover, agents, self.goals))
        return s

    def get_state(self):
        return self.pmap.flatten()

    def step(self, action, agent):  #calculate reward
        done = False

        ix = []
        iy = []
        for o in range(self.agent_n):
            ix.append(agent.ixs[o])
            iy.append(agent.iys[o])
        ix_ori = copy.deepcopy(ix)
        iy_ori = copy.deepcopy(iy)
        reward = [-0.5] * self.agent_n # move one step，no success -0.5

        for o in range(self.agent_n):
            minix = int(ix[o] + self.motion[action[o]][0])
            miniy = int(iy[o] + self.motion[action[o]][1])
            ix[o] = minix
            iy[o] = miniy

        crash_reward = 100 #Fail the game，reward-100
        for o in range(self.agent_n):
            if detect(ix[o], iy[o], self.ox, self.oy):
                reward[o] -= crash_reward
                # print('find obs')
                done = True
        for o in range(self.agent_n):
            if ix[o] == 0 or ix[o] == (AREA_WIDTH - 1) or iy[o] == 0 or iy[o] == (AREA_WIDTH - 1):
                reward[o] -= crash_reward  #out of the map
                # print('out of range')
                done = True


        for o in range(self.agent_n):
            agent.ixs[o] = ix[o]
            agent.iys[o] = iy[o]

        for o in range(self.agent_n):
            for p in range(o):
                if agent.ixs[o] == agent.ixs[p] and agent.iys[o] == agent.iys[p]:
                    reward[o] -= crash_reward
                    reward[p] -= crash_reward
                    done = True
                    print('crash')
                    self.crash = 1

        d = [100] * self.agent_n
        for n in range(self.agent_n):
            for m in range(len(self.goals)):
                d[n] = min(d[n], cal_dis(ix[n], iy[n], self.goals[m].x, self.goals[m].y))

        if max(d) <= 1:  #Find rule
            done = True
            print('find')
            self.finish = 1
            for i in range(self.agent_n):
                reward[i] += 200  #Success reward +200

        if self.show_animation:
            self.plot_figure(self.pmap)
            # plt.plot(ix_ori, iy_ori, "kv")
            plt.plot(ix, iy, ".r") #draw hunters
            plt.pause(0.5) # pause0.5s

        if self.t > 50:
            done = True
        for i in range(self.agent_n):
            reward[i] += -0.5 #move one step reward-0.5
            new_dis = np.linalg.norm([agent.ixs[i] - self.goals[0].x,agent.iys[i] - self.goals[0].y])
            reward[i] += self.dis_list[i] - new_dis
            self.dis_list[i] = new_dis
        self.rewards += sum(reward)
        if done == True:
            done = 1


        return sum(reward), done
