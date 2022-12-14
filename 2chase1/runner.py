import numpy as np
import os
from common.rollout import RolloutWorker, CommRolloutWorker
from agent.agent import Agents, CommAgents
from common.replay_buffer import ReplayBuffer
import matplotlib.pyplot as plt


class Runner:
    def __init__(self, env, args):
        self.env = env
        if args.alg.find('commnet') > -1 or args.alg.find('g2anet') > -1:  # communication agent
            self.agents = CommAgents(args)
            self.rolloutWorker = CommRolloutWorker(env, self.agents, args)
        else:  # no communication agent
            self.agents = Agents(args)
            self.rolloutWorker = RolloutWorker(env, self.agents, args)
        if args.learn and args.alg.find('coma') == -1 and args.alg.find('central_v') == -1 and args.alg.find('reinforce') == -1:  # these 3 algorithms are on-poliy
            self.buffer = ReplayBuffer(args)
        self.args = args
        self.finish_rates = []
        self.crash_rates = []
        self.episode_rewards = []

        # 用来保存plt和pkl
        self.save_path = self.args.result_dir + '/' + args.alg + '/' + args.map
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def run(self, num):
        train_steps = 0
        # print('Run {} start'.format(num))
        for epoch in range(1,self.args.n_epoch):
            print('Run {}, train epoch {}'.format(num, epoch))
            if epoch % self.args.evaluate_cycle == 0:
                crash_rate, finish_rate, episode_reward = self.evaluate()
                # print('win_rate is ', win_rate)
                self.finish_rates.append(finish_rate)
                self.crash_rates.append(crash_rate)
                self.episode_rewards.append(episode_reward)
                # self.plt(num)

            episodes = []
            # collect self.args.n_episodes个episodes
            for episode_idx in range(self.args.n_episodes):
                episode, _, _ = self.rolloutWorker.generate_episode(episode_idx)
                episodes.append(episode)
                # print(_)
            # Each item in the episode is a: (1, episode_len, n_agents, Specific dimensions)A four-dimensional array with all the episode's obs put together below
            episode_batch = episodes[0]
            episodes.pop(0)
            for episode in episodes:
                for key in episode_batch.keys():
                    episode_batch[key] = np.concatenate((episode_batch[key], episode[key]), axis=0)
            if self.args.alg.find('coma') > -1 or self.args.alg.find('central_v') > -1 or self.args.alg.find('reinforce') > -1:
                self.agents.train(episode_batch, train_steps, self.rolloutWorker.epsilon)
                train_steps += 1
            else:
                self.buffer.store_episode(episode_batch)
                for train_step in range(self.args.train_steps):
                    mini_batch = self.buffer.sample(min(self.buffer.current_size, self.args.batch_size))
                    self.agents.train(mini_batch, train_steps)
                    train_steps += 1
        self.plt(num)

    def evaluate(self):
        finish_number = 0
        crash_number = 0
        episode_rewards = 0
        for epoch in range(self.args.evaluate_epoch):
            _, episode_reward, win_tag = self.rolloutWorker.generate_episode(epoch, evaluate=True)
            episode_rewards += episode_reward
            crash_number += win_tag[0]
            finish_number += win_tag[1]
        return crash_number / self.args.evaluate_epoch, finish_number / self.args.evaluate_epoch, episode_rewards / self.args.evaluate_epoch

    def plt(self, num): #plot statistics
        plt.figure()
        plt.axis([0, self.args.n_epoch, 0, 100])
        plt.cla()
        plt.plot(range(len(self.episode_rewards)), self.episode_rewards)
        plt.xlabel('epoch*{}'.format(self.args.evaluate_cycle))
        plt.ylabel('episode_rewards')
        plt.savefig(self.save_path + '/plt_{}.png'.format(num), format='png')
        np.save(self.save_path + '/episode_rewards_{}'.format(num), self.episode_rewards)

        plt.figure()
        plt.axis([0, self.args.n_epoch, 0, 100])
        plt.cla()
        plt.plot(range(len(self.finish_rates)), self.finish_rates)
        plt.xlabel('epoch*{}'.format(self.args.evaluate_cycle))
        plt.ylabel('episode_finish')
        plt.savefig(self.save_path + '/finish_{}.png'.format(num), format='png')
        np.save(self.save_path + '/episode_finish_{}'.format(num), self.finish_rates)


        plt.figure()
        plt.axis([0, self.args.n_epoch, 0, 100])
        plt.cla()
        plt.plot(range(len(self.crash_rates)), self.crash_rates)
        plt.xlabel('epoch*{}'.format(self.args.evaluate_cycle))
        plt.ylabel('episode_crash')

        plt.savefig(self.save_path + '/crash_{}.png'.format(num), format='png')
        np.save(self.save_path + '/episode_crash_{}'.format(num), self.crash_rates)









